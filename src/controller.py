from time import sleep
import cv2
import pyautogui
from numpy import array
from PIL.ImageGrab import grab

from src.core.board import Board
from src.vision.img_proc import ImageProcessor, BoardNotFoundError, AbnormalBoardError
from src.vision.display import Display
from src.algorithms.solver import Solver, Win
from src.util.time import Time
from src.util.settings import Settings
from src.util.logger import Type

# screen shot -> process image -> solve -> clicks

class MinesweeperAI(Settings):
    def __init__(self):
        self.board = Board()
        self.timer = Time()
        self.image_processor = ImageProcessor(self.board, self.timer)
        self.display = Display(self.image_processor)
        self.solver = Solver(self.board, self.timer)

    def run(self):
        while (True):
            try:
                self.step()
            except BoardNotFoundError:
                print("board not found")
            except AbnormalBoardError as e:
                print(f"more than {ImageProcessor.UNRECOGNIZE_COUNT} cells have unrecognized colors")
                self.reset()
                MinesweeperAI.halt()
            except pyautogui.FailSafeException:
                print("PyAutoGUI failsafe triggered (mouse moved to corner)")
                MinesweeperAI.halt()
            except Win:
                print("congratulations! the board has been solved!")
                self.solver.log(self.solver.solve_count, Type.SOLVE_COUNT)
                self.timer.log(self.timer.process_time, Type.TIME_ANALYSIS)
                self.reset()
                MinesweeperAI.halt()

    def step(self):
        sleep(MinesweeperAI.SLEEP_TIME)
        # screen shot
        img = MinesweeperAI.screen_shot()

        # process image
        self.image_processor.process(img)

        self.display.display()

        # solve
        self.solver.solve()

    def reset(self):
        self.board.reset()
        self.solver.reset()

    @staticmethod
    def screen_shot():
        img = grab()
        img_arr = array(img)
        img_arr = cv2.cvtColor(img_arr, cv2.COLOR_RGB2BGR)
        return img_arr

    @staticmethod
    def halt():
        response = ''
        while response not in {'r', 'q'}:
            response = input("Program halted. Enter r to resume, q to quit: ").strip().lower()
        if response == 'r':
            return
        elif response == 'q':
            exit(0)

# timing analysis?
# how many cells are attributed to each algorithm? (straightfwd, setelim, constraintsearch)

# documentation (readme)
# upload to github

# resume
# OOP
# Display
# MVC
# Error handling with Exceptions
# Logging
# demonstrate more on website
