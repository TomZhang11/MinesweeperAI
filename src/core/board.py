from src.core.screen_object import ScreenObject
from src.core.cell import Cell

class Board(ScreenObject):
    ROWS_TO_MINES = {8: 10, 14: 40, 20: 99}

    def __init__(self):
        super().__init__()
        self.rows = 0
        self.columns = 0
        self.cells = []
        # flag mutated by the image processor to quickly act if board is new (all cells are not opened)
        self.new = True
        self.mines_remaining = 0

    def init(self, dim):
        # initializing each cell
        for i in range(self.rows):
            self.cells.append([])
            for j in range(self.columns):
                self.cells[i].append(Cell(self.x, self.y, i, j, dim))

        # adding neighbors to each cell
        for i in range(self.rows):
            for j in range(self.columns):
                for r, c in [(i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1), (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1)]:
                    if self.valid_pos(r, c):
                        self.cells[i][j].neighbors.append(self.cells[r][c])

        self.mines_remaining = Board.ROWS_TO_MINES[self.rows]
        self.unopened_remaining = self.rows * self.columns - self.mines_remaining

    def reset(self):
        super().__init__()
        self.rows = 0
        self.columns = 0
        self.cells = []
        self.new = True

    def valid_pos(self, r, c):
        return r >= 0 and r < self.rows and c >= 0 and c < self.columns

    def __str__(self):
        return f"Board(x={self.x}, y={self.y}, w={self.w}, h={self.h}, rows={self.rows}, columns={self.columns})"
        # result = []
        # for row in self.cells:
        #     row_str = []
        #     for cell in row:
        #         if cell.state == State.UNOPENED:
        #             row_str.append("□")
        #         elif cell.state == State.FLAGGED:
        #             row_str.append("⚑")
        #         else:
        #             row_str.append(str(cell.num))
        #     result.append(" ".join(row_str))
        # return "\n".join(result)
