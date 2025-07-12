import pyautogui

class ScreenObject:
    def __init__(self, x = 0, y = 0, w = 0, h = 0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.cent_x = x + (w // 2)
        self.cent_y = y + (h // 2)

    def click(self):
        pyautogui.click(self.cent_x / 2, self.cent_y / 2)

    def right_click(self):
        pyautogui.rightClick(self.cent_x / 2, self.cent_y / 2)
