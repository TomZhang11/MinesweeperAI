from src.util.logger import Logger, Type
from src.algorithms.basic import BasicSolver
from src.algorithms.set import SetSolver
from src.algorithms.constraint import ConstraintSolver
from src.core.cell import State

class Win(Exception):
    pass

# I use 3 different algorithms to solve minesweeper
# 1. simple algorithm
# 2. set elimination algorithm
# 3. constraint search

# 1 cannot handle all cases that 2 can handle, and 2 cannot handle all cases 3 can handle
# but 1, 2, 3 increases in computational expense
# so first use 1 to solve easy cases, then 2, 3

class Solver(Logger):
    def __init__(self, board, timer):
        self.board = board
        self.iterations = 0
        self.boundary_nums = [] # boundary cells with numbers on it that will be useful when running the algorithms
        self.timer = timer
        self.basic_solver = BasicSolver(self.board, self.boundary_nums, self.timer)
        self.set_elim_solver = SetSolver(self.board, self.boundary_nums, self.timer)
        self.constraint_solver = ConstraintSolver(self.board, self.boundary_nums, self.timer)
        self.unopened_count = 0
        self.solve_count = {"basic": {"open": 0, "flag": 0}, "set": {"open": 0, "flag": 0}, "constraint": {"open": 0, "flag": 0}}

    def solve(self):
        # update iterations and log
        self.log(self.iterations, Type.ITERATION)
        self.iterations += 1

        # new board, click center
        if self.board.new:
            self.board.click()
            self.board.click()
            return

        self.find_boundary_nums()

        # simple algorithm
        self.basic_solver.run()

        # set elimination algorithm
        self.set_elim_solver.run()

        # constraint seach
        self.constraint_solver.run()

        total = self.tally()
        if not total: # neither solver could solve
            # end game situation
            self.constraint_solver.end_game()
        if self.unopened_count == total: # win logic
            raise Win

    def reset(self):
        self.iterations = 0
        self.basic_solver.reset()
        self.set_elim_solver.reset()
        self.constraint_solver.reset()

    def tally(self):
        # fetch
        basic_opened = self.basic_solver.solve_count["open"]
        basic_flagged = self.basic_solver.solve_count["flag"]
        set_opened = self.set_elim_solver.solve_count["open"]
        set_flagged = self.set_elim_solver.solve_count["flag"]
        constraint_opened = self.constraint_solver.solve_count["open"]
        constraint_flagged = self.constraint_solver.solve_count["flag"]
        
        # calculate totals
        total_opened = basic_opened + set_opened + constraint_opened
        total_flagged = basic_flagged + set_flagged + constraint_flagged

        # update board
        self.board.mines_remaining -= total_flagged

        # reset
        self.basic_solver.reset()
        self.set_elim_solver.reset()
        self.constraint_solver.reset()

        # update solve count
        self.solve_count["basic"]["open"] += basic_opened
        self.solve_count["basic"]["flag"] += basic_flagged
        self.solve_count["set"]["open"] += set_opened
        self.solve_count["set"]["flag"] += set_flagged
        self.solve_count["constraint"]["open"] += constraint_opened
        self.solve_count["constraint"]["flag"] += constraint_flagged

        return total_opened + total_flagged

    def find_boundary_nums(self):
        self.boundary_nums.clear()
        self.unopened_count = 0
        for row in self.board.cells:
            for cell in row:
                if cell.num > 0 and len(cell.unopened_neighbors()):
                    self.boundary_nums.append(cell)
                elif cell.state == State.UNOPENED:
                    self.unopened_count += 1
        self.unopened_count
