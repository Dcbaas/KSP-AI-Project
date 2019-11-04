import pyautogui

class MemoryManager:
    def __init__(self, quit_btn_location = (0,0), move_duration = 0.25, run_limit = 50):
        pyautogui.PAUSE = 1
        pyautogui.FAILSAFE = True

        self.QUIT_BTN_LOCATION = quit_btn_location #TODO: What is this location.
        self.MOVE_DURATION = move_duration
        self.RUN_LIMIT = run_limit

        self.run_round = 0

    def _reset_ksp(self):
        pyautogui.press('esc')
        pyautogui.moveTo(self.QUIT_BTN_LOCATION[0], self.QUIT_BTN_LOCATION,
        duration=self.MOVE_DURATION)
        #TODO Implement the rest of this function. 
        


