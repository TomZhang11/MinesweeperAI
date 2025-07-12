import cv2
from src.core.cell import State
from src.util.logger import Logger, Type
from src.util.time import Process
from src.util.settings import Settings

class BoardNotFoundError(Exception):
    pass

class AbnormalBoardError(Exception):
    pass

class ImageProcessor(Logger, Settings):
    def __init__(self, board, timer):
        self.img = None
        self.board = board
        self.blur = None
        self.thresh = None
        self.roi = None
        self.roi_thresh = None
        self.timer = timer

    # gray blur thresh
    def preprocess(self):
        if self.img is None:
            return
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.blur = cv2.GaussianBlur(gray, (3, 3), 0)
        _, self.thresh = cv2.threshold(self.blur, 183, 255, cv2.THRESH_BINARY_INV)

    # find x, y, w, h
    # findContours then find based on area
    def find_board(self):
        # board already found
        if self.board.w != 0:
            return

        if self.thresh is None:
            return
        
        # find x, y, w, h of board
        contours, _ = cv2.findContours(self.thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 600000 and area < 1200000:
                self.board.x, self.board.y, self.board.w, self.board.h = cv2.boundingRect(contour)
                self.board.cent_x = self.board.x + (self.board.w // 2)
                self.board.cent_y = self.board.y + (self.board.h // 2)
                return
        
        # board not found
        raise BoardNotFoundError

    # zoom in on the board
    def focus(self):
        if self.img is None or self.blur is None:
            return
        self.roi = self.img[self.board.y : self.board.y + self.board.h, self.board.x : self.board.x + self.board.w]
        roi_blur = self.blur[self.board.y : self.board.y + self.board.h, self.board.x : self.board.x + self.board.w]
        _, self.roi_thresh = cv2.threshold(roi_blur, 190, 255, cv2.THRESH_BINARY_INV)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        self.roi_thresh = cv2.dilate(self.roi_thresh, kernel, iterations=1)

    # extract rows, columns info
    # initialize cells
    # use findContours approach
    def find_cells(self):
        if self.board.rows != 0 or self.roi_thresh is None or self.roi is None:
            return

        # find rows and columns of board
        contours, _ = cv2.findContours(self.roi_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 2000 and area < 8000:
                _, _, dim, _ = cv2.boundingRect(contour)
                dim += 2
                break
        self.board.rows = round(self.roi.shape[0] / dim)
        self.board.columns = round(self.roi.shape[1] / dim)
        self.board.init(dim)

    # extract cell states and numbers from image
    # reads color of center pixel, uses a preconfigured mapping
    def read_board(self):
        # green values for unopened tiles
        G_VALS = {214, 208, 224, 220}
        # mapping from red values to numbers
        R_MAP = {
            223: 0, 210: 0,
            56: 1,
            80: 2,
            194: 3,
            217: 4,
            205: 4,
            235: 5,
            237: 5,
            238: 5,
            75: 6,
            76: 6,
            66: 7,
        }

        if self.img is None:
            return

        unrecognized_color_count = 0
        for row in self.board.cells:
            for cell in row:
                g = int(self.img[cell.cent_y, cell.cent_x, 1])
                r = int(self.img[cell.cent_y, cell.cent_x, 2])

                # not opened
                if g in G_VALS:
                    if cell.state != State.FLAGGED:
                        cell.state = State.UNOPENED
                        cell.num = -1
                    continue

                # opened
                cell.state = State.OPENED
                cell.num = R_MAP.get(r, -1)
                if cell.num == -1:
                    # unrecognized color
                    cell.state = State.UNRECOGNIZED
                    b = self.img[cell.cent_y, cell.cent_x, 0]
                    self.log(f"{cell} has unrecognized bgr({b}, {g}, {r})", Type.ABNORMAL)
                    unrecognized_color_count += 1
                else:
                    self.board.new = False

                # abnormal board
                if unrecognized_color_count >= ImageProcessor.UNRECOGNIZE_COUNT:
                    raise AbnormalBoardError

    def process(self, img):
        self.timer.start()
        self.img = img
        self.preprocess()
        self.find_board()
        self.focus()
        self.find_cells()
        self.read_board()
        if self.board.new:
            self.log("")
            self.log("board found!")
            self.log(self.board)
        self.timer.end(Process.IMG_PROC)
