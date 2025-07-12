from src.core.cell import State
from src.util.time import Process

# set elimination algorithm, intermediate logic
# looks at a cell's number, then for each of the neighbors, looks at their numbers, and do set subtractions to try to obtain results
# example:
#  +---+---+---+
#  |   |   |   | <- mine here
#  +---+---+---+
#  | 1 | 3 |   | <- mine here
#  +---+---+---+
# 3 - 1 = 2
# unopened neighbors of 3 = {(0, 1), (1, 1) (2, 0) (2, 1)}
# unopened neighbors of 1 = {(0, 1), (1, 1)}
# difference = unopened neighbors of 3 - unopened neighbors of 1 = {(2, 0) (2, 1)}
# 3 - 1 = 2 = len(difference), so cells in difference are mines
# another example:
#  +---+---+---+
#  |   |   |   | <- safe here
#  +---+---+---+
#  | 1 | 1 |   | <- safe here
#  +---+---+---+
# unopened neighbors of (0, 0) = {(0, 1), (1, 1)}
# unopened neighbors of (1, 0) = {(0, 1), (1, 1), (2, 0), (2, 1)}
# difference = {(2, 0), (2, 1)}
# 1 - 1 = 0, but len(difference) = 2, so all cells in difference are safe
class SetSolver:
    def __init__(self, board, boundary_nums, timer):
        self.board = board
        self.boundary_nums = boundary_nums
        self.timer = timer
        self.solve_count = {"open": 0, "flag": 0}
    
    def run(self):
        self.timer.start()
        # set elimination algorithm on each of the boundary cells
        for cell in self.boundary_nums:
            self.set_elim(cell)
        self.timer.end(Process.SET)

    def reset(self):
        self.solve_count = {"open": 0, "flag": 0}

    def set_elim(self, cell):
        for neighbor in cell.opened_neighbors():
            # the logic becomes a bit more complicated when neighbor has any unique cells,
            # and when flags are taken into consideration
            # will not explain here
            unopened_neighbors = cell.unopened_neighbors()
            if not unopened_neighbors:
                return

            s1 = set(unopened_neighbors + cell.flagged_neighbors())
            nbor_flag = neighbor.flagged_neighbors()
            s2 = set(neighbor.unopened_neighbors() + nbor_flag)
            unique1 = s1 - s2
            if not unique1:
                continue
            # assume unique2 is all mines here, this will make num2 smaller thus diff bigger, if this still produces a diff of 0, then all unique1 is safe
            unique2 = s2 - s1
            num2 = neighbor.num - len(unique2 | set(nbor_flag)) # num2 - (unique2 + mines2)
            num1 = cell.num - cell.flag_count # num1 - mines1
            diff = num1 - num2
            if diff == 0:
                for c in unique1:
                    if c.state != State.UNOPENED:
                        continue
                    c.open()
                    self.solve_count["open"] += 1
                return

            # assume unique2 is all safe, will make num2 bigger thus diff smaller, if this still produces a diff equal to unique1, then all unique1 are mines
            num2 = neighbor.num - len(nbor_flag)
            diff = num1 - num2
            if diff == len(unique1):
                for c in unique1:
                    c.flag()
                    self.solve_count["flag"] += 1
