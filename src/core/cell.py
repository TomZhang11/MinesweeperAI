from src.core.screen_object import ScreenObject
from enum import Enum
from src.util.logger import Logger, Type

class State(Enum):
    UNOPENED = 0
    OPENED = 1
    FLAGGED = 2

class Cell(ScreenObject, Logger):
    def __init__(self, board_x, board_y, row, col, dim):
        # screen info
        self.offset_x = col * dim
        self.offset_y = row * dim
        super().__init__(board_x + self.offset_x, board_y + self.offset_y, dim, dim)

        # board info
        self.row = row
        self.col = col

        # state
        self.state = State.UNOPENED
        self.num = -1

        # neighbors
        self.flag_count = 0 # number of flagged neighbors
        self.neighbors = []

    def open(self):
        # if self.state != State.UNOPENED:
        #     return
        self.click()
        self.log(self, Type.OPEN)
        self.state = State.OPENED

    def flag(self):
        # if self.state != State.UNOPENED:
        #     return
        self.right_click()
        self.log(self, Type.FLAG)
        self.state = State.FLAGGED
        # notify neighbors
        for cell in self.neighbors:
            cell.flag_count += 1

    def unopened_neighbors(self):
        return [cell for cell in self.neighbors if cell.state == State.UNOPENED]
    
    def opened_neighbors(self):
        return [cell for cell in self.neighbors if cell.state == State.OPENED and cell.num > 0] # opened with a positive number

    def flagged_neighbors(self):
        return [cell for cell in self.neighbors if cell.state == State.FLAGGED]

    def __str__(self):
        return f"Cell(row={self.row}, col={self.col}, state={self.state}, num={self.num})"
