from src.util.time import Process

# straight forward algorithm, mimics how a human would play
# implements two basic logics by looking at a number's unopened neighbors count and flagged neighbors count
# 1. if the number on a cell is equal to the number of flagged neighbors, then all other unopened neighbors are safe
# 2. if the number of a cell is equal to the number of unopened neighbors, then all unopened neighbors are mines
class BasicSolver:
    def __init__(self, board, boundary_nums, timer):
        self.board = board
        self.boundary_nums = boundary_nums
        self.timer = timer
        self.solve_count = {"open": 0, "flag": 0}

    def run(self):
        self.timer.start()
        # straight forward algorithm on each of the boundary cells
        for cell in self.boundary_nums:
            self.straight_fwd(cell)
        self.timer.end(Process.SIMPLE)

    def reset(self):
        self.solve_count = {"open": 0, "flag": 0}

    def straight_fwd(self, cell):
        unopened_neighbors = cell.unopened_neighbors()
        if len(unopened_neighbors) == 0: # return if no unopened neighbors to open or flag
            return

        if cell.num == cell.flag_count: # number is satisfied, open the rest of the neighbors
            for neighbor in unopened_neighbors:
                neighbor.open()
                self.solve_count["open"] += 1
        elif cell.num == len(unopened_neighbors) + cell.flag_count: # all neighbors are mines
            for neighbor in unopened_neighbors:
                neighbor.flag()
                self.solve_count["flag"] += 1
