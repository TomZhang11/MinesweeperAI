from enum import Enum
from time import time
from src.util.logger import Logger

class Process(Enum):
    IMG_PROC = "img_proc"
    SIMPLE = "simple_solver"
    SET = "set_solver"
    CONSTRAINT = "constraint_solver"

class Time(Logger):
    def __init__(self):
        self.process_time = {"img_proc": 0.0, "simple_solver": 0.0, "set_solver": 0.0, "constraint_solver": 0.0}
        self.time = 0.0

    def start(self):
        self.time = time()

    def end(self, process):
        self.process_time[process.value] += time() - self.time
