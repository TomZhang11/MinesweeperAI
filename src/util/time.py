from enum import Enum
from time import time
from src.util.logger import Logger

# tracking time it takes for difference processes to complete

class Process(Enum):
    IMG_PROC = "image processing"
    SIMPLE = "simple solver"
    SET = "set solver"
    CONSTRAINT = "constraint solver"

class Time(Logger):
    def __init__(self):
        self.process_time = {"image processing": 0.0, "simple solver": 0.0, "set solver": 0.0, "constraint solver": 0.0}
        self.time = 0.0

    def start(self):
        self.time = time()

    def end(self, process):
        self.process_time[process.value] += time() - self.time
