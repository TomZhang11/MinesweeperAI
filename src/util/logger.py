from enum import IntEnum

# centralized logging

class Type(IntEnum):
    ABNORMAL = 1
    OPEN = 0
    FLAG = 0
    ITERATION = 4
    PLAIN = 5
    SOLVE = 6
    TIME_ANALYSIS = 7
    SOLVE_COUNT = 8

def print_abnormal(msg: str) -> None:
    print(msg)

def print_open(cell: object) -> None:
    print(f"{cell} is opened")

def print_flag(cell: object) -> None:
    print(f"{cell} is flagged")

def print_iteration(iterations: int) -> None:
    if iterations == 0:
        print("opening center cell")
    else:
        print("")
        print(f"iteration {iterations} --------------------")

def print_plain(msg: str) -> None:
    print(msg)

def print_solve(msg: str) -> None:
    print(msg)

def print_timing(process_time: dict[str, float]) -> None:
    print()
    print("timing analysis:")
    for process in process_time:
        print(f"{process}: {process_time[process]:.3f}s")
    print()

def print_solve_count(solve_count: dict[str, dict[str, int]]) -> None:
    print()
    print("solve count:")
    for algorithm in solve_count:
        print(f"{algorithm}: {solve_count[algorithm]}")

class Logger:
    @staticmethod
    def log(obj, type=Type.PLAIN):
        if not type:
            return
        if type == Type.ABNORMAL:
            print_abnormal(obj)
        elif type == Type.OPEN:
            print_open(obj)
        elif type == Type.FLAG:
            print_flag(obj)
        elif type == Type.ITERATION:
            print_iteration(obj)
        elif type == Type.PLAIN:
            print_plain(obj)
        elif type == Type.SOLVE:
            print_solve(obj)
        elif type == Type.TIME_ANALYSIS:
            print_timing(obj)
        elif type == Type.SOLVE_COUNT:
            print_solve_count(obj)
