from enum import IntEnum

class Type(IntEnum):
    ABNORMAL = 1
    OPEN = 0
    FLAG = 0
    ITERATION = 4
    PLAIN = 5
    TIME_ANALYSIS = 6
    SOLVE_COUNT = 7

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

def print_timing(process_time: dict[str, float]) -> None:
    print("timing analysis:")
    for process in process_time:
        print(f"{process}: {process_time[process]}s")

def print_solve_count(solve_count: dict[str, dict[str, int]]) -> None:
    print("solve count:")
    for algorithm in solve_count:
        print(f"{algorithm}: {solve_count[algorithm]}")

class Logger:
    @staticmethod
    def log(obj, type=Type.PLAIN):
        if not type:
            return
        match type:
            case Type.ABNORMAL:
                print_abnormal(obj)
            case Type.OPEN:
                print_open(obj)
            case Type.FLAG:
                print_flag(obj)
            case Type.ITERATION:
                print_iteration(obj)
            case Type.PLAIN:
                print_plain(obj)
            case Type.TIME_ANALYSIS:
                print_timing(obj)
            case Type.SOLVE_COUNT:
                print_solve_count(obj)
