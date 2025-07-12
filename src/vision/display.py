import cv2

class Display:
    def __init__(self, image_processor):
        self.image_processor = image_processor
        cv2.namedWindow("Computer Vision", cv2.WINDOW_NORMAL)

    def display(self):
        board = self.image_processor.board
        roi = self.image_processor.roi

        for row in board.cells:
            for cell in row:
                cv2.rectangle(roi, (cell.offset_x, cell.offset_y), (cell.offset_x + cell.w , cell.offset_y + cell.h), (0, 255, 0), 2)
        cv2.imshow("Computer Vision", roi)
        cv2.waitKey(1)
