import pyautogui

# centralized settings

class Settings:
    SPEED = "fast" # fast medium slow

    # the number of unrecognized cell colors before throwing an exception
    UNRECOGNIZE_COUNT = 70

    SLEEP_TIME = 2

    if SPEED == "fast":
        SLEEP_TIME = 0.7
        UNRECOGNIZE_COUNT = 30
    elif SPEED == "medium":
        SLEEP_TIME = 1
        UNRECOGNIZE_COUNT = 50

    pyautogui.PAUSE = 0
