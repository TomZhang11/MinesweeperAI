import pyautogui

class Settings:
    SPEED = "slow" # fast medium slow

    # the number of unrecognized cell colors before throwing an exception
    UNRECOGNIZE_COUNT = 70

    SLEEP_TIME = 2
    FLAG = True

    if SPEED == "fast":
        SLEEP_TIME = 0.65
        UNRECOGNIZE_COUNT = 20
        FLAG = False
    elif SPEED == "medium":
        SLEEP_TIME = 1
        UNRECOGNIZE_COUNT = 50

    pyautogui.PAUSE = 0
