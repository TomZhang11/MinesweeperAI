from src.core.cell import Cell, State
from src.util.time import Process
from src.util.logger import Logger, Type

# iterate through all possible arrangement of the game board
# if a cell is a mine every time, then it is 100% a mine
# if a cell is safe every time, then it is safe

# an arrangement is possible means it satisfies 2 constraints:
# 1. there will not be a cell where there are more flags than the number on it
# 2. there will not be a cell where there are less flags than the number on it

class ConstraintSolver(Logger):
    def __init__(self, board, boundary_nums, timer):
        self.board = board
        self.boundary_nums = boundary_nums
        self.timer = timer
        self.solve_count = {"open": 0, "flag": 0}

    def run(self):
        self.timer.start()
        # find paths for constraint search to iterate through
        paths = self.find_paths()

        self.constraint_search(paths)
        self.timer.end(Process.CONSTRAINT)

    def reset(self):
        self.solve_count = {"open": 0, "flag": 0}

    def constraint_search(self, paths: list[list[Cell]]):
        for path in paths: # for each path
            self.log(f"length of constraint search: {len(path)}", Type.SOLVE)
            arrangements_count = {cell: 0 for cell in path} # stores how many times a cell appears as a mine
            total_arrangements = ConstraintSolver.iterate(path, set(), arrangements_count, self.board.mines_remaining) # use constraint search to iterate through the path, updating arrangements_count when a possible arrangement is found

            # react upon results
            for cell in arrangements_count:
                if arrangements_count[cell] == 0: # if a cell is safe in all arrangements, then it is 100% safe
                    cell.open()
                    self.solve_count["open"] += 1
                elif arrangements_count[cell] == total_arrangements: # if a cell is a mine in all arrangements, then it is 100% a mine
                    cell.flag()
                    self.solve_count["flag"] += 1

    def end_game(self):
        unopened = self.find_unopened()
        if len(unopened) > 20: # don't want to iterate more than 2^20 times
            return
        self.constraint_search([unopened])

    # O(2^n)
    @staticmethod
    def iterate(path: list[Cell], virtual_flags: set[Cell], arrangements_count: dict[Cell, int], mines_remaining: int) -> int:
        # virtual_flags contains the set of cells that have been pretended to be a mine in the past
        # think of path as the future, virtual_flags as the past
        if mines_remaining < 0: return 0
        if not path: # base case: path empty
            for cell in virtual_flags: # add 1 for each cell that ended up as a mine
                arrangements_count[cell] += 1
            return 1

        cell = path.pop()
        total_arrangements = 0
        # tree pruning
        # only move forward if it will result in a possible world
        if possibly_mine(cell, virtual_flags): # if it is possible for this cell to be a mine
            virtual_flags.add(cell)
            total_arrangements += ConstraintSolver.iterate(path, virtual_flags, arrangements_count, mines_remaining - 1) # move forward pretending this cell 
            virtual_flags.remove(cell)
        if possibly_safe(cell, set(path), virtual_flags): # if it is possible for this cell to be safe
            total_arrangements += ConstraintSolver.iterate(path, virtual_flags, arrangements_count, mines_remaining) # move forward pretending this cell is safe
        path.append(cell)
        return total_arrangements

    def find_paths(self) -> list[list[Cell]]:
        # boundary unopened cells to iterate over
        boundary_unopened_cells = set()
        for cell in self.boundary_nums:
            for unopened_neighbor in cell.unopened_neighbors():
                boundary_unopened_cells.add(unopened_neighbor)

        # divide boundary into smaller paths for efficiency
        # the idea is that 2^10 + 2^7 is smaller than 2^17
        paths = []
        while boundary_unopened_cells:
            paths.append(find_path(boundary_unopened_cells.pop(), set(), boundary_unopened_cells))
            boundary_unopened_cells -= set(paths[-1])
        return paths

    def find_unopened(self):
        unopened = []
        for row in self.board.cells:
            for cell in row:
                if cell.state == State.UNOPENED:
                    unopened.append(cell)
        return unopened

# determines if it is possible for this cell to be a mine
# need to satisfy the constraint that:
# there will not be a cell where there are more flags than the number on it
def possibly_mine(cell: Cell, virtual_flags: set[Cell]) -> bool:
    # cell not in virtual_flags
    for opened in cell.opened_neighbors(): # for each opened neighbors
        virtual_flags_count = 0
        for unopened in opened.unopened_neighbors():
            if unopened in virtual_flags:
                virtual_flags_count += 1
        if opened.flag_count + virtual_flags_count == opened.num: # if flag count + virtual flags count already equal number, then you cannot have one more mine
            return False
    return True

# determines if it is possible for this cell to be safe
# need to satisfy the constraint that:
# there will not be a cell where there are less flags than the number on it
def possibly_safe(cell: Cell, path: set[Cell], virtual_flags: set[Cell]) -> bool:
    # cell not in path and not in virtual_flags
    for opened in cell.opened_neighbors(): # for each opened neighbors
        possible_mine_locations = 0
        virtual_flags_count = 0
        for unopened in opened.unopened_neighbors():
            if unopened in path:
                possible_mine_locations += 1
            elif unopened in virtual_flags:
                virtual_flags_count += 1
        if opened.flag_count + virtual_flags_count + possible_mine_locations + 1 == opened.num: # if all possible mine locations + this cell meets the number, then you cannot have that this cell is not a mine, ie, proceed pretending this is safe
            return False
    return True

#   +---+---+---+
# [ |   |   |   | ] <- need to return this path
#   +---+---+---+
#   | 1 | 1 | 1 |
#   +---+---+---+
def find_path(cur: Cell, prev: set[Cell], boundary_unopened_cells: set[Cell]) -> list[Cell]:
    # dfs
    prev.add(cur)
    path = [cur]
    bidirectional = False
    for opened_neighbor in cur.opened_neighbors():
        for unopened_neighbor in opened_neighbor.unopened_neighbors():
            if unopened_neighbor in prev or unopened_neighbor not in boundary_unopened_cells: # only continue if it's not in prev and it's a boundary cell
                continue
            directional_path = find_path(unopened_neighbor, prev, boundary_unopened_cells)
            if bidirectional: # you landed in the middle
                # need to reverse the left path and add it to the front
                directional_path.reverse()
                path = directional_path + path
            else:
                path += directional_path
                bidirectional = True
    return path
