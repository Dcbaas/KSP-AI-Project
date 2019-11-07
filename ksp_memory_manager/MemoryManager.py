import pyautogui
import time

class MemoryManager:
    def __init__(self, btn_location_dic = None, move_duration = 0.25, run_limit = 50):
        pyautogui.PAUSE = 3
        pyautogui.FAILSAFE = True

        if btn_location_dic is None:
            raise Exception('You must specify the locations of the buttons for exiting')

        self.QUIT_BTN_LOCATION = btn_location_dic['quit_btn']
        self.BACK_BTN_LOCATION = btn_location_dic['back_btn']
        self.FINAL_QUIT_BTN = btn_location_dic['final_quit_btn']
        self.QUIT_TO_MAIN_BTN_LOCATION = btn_location_dic['quit_to_main_btn']
        self.MOVE_DURATION = move_duration
        self.RUN_LIMIT = run_limit

        self.run_round = 0

    def reload_ksp(self):
        pyautogui.keyDown('f9')
        time.sleep(3.0)
        pyautogui.keyUp('f9')

    def restart_ksp(self):
        self.reload_ksp()
        print('Quitting to Main Menu')
        pyautogui.press('esc')

        x, y = self.QUIT_TO_MAIN_BTN_LOCATION
        pyautogui.moveTo(x, y)
        pyautogui.click()

        print('Exiting')
        x, y = self.BACK_BTN_LOCATION
        pyautogui.moveTo(x, y)
        pyautogui.click()

        x, y = self.QUIT_BTN_LOCATION
        pyautogui.moveTo(x, y)
        pyautogui.click()

        x, y = self.FINAL_QUIT_BTN
        pyautogui.moveTo(x, y)
        pyautogui.click()

        # TODO: Finish this off. Need to restart game and navigate back to running game.
        print('Sequence Finished')
        
if __name__ == "__main__":
    btn_loc_dictionary = {'quit_btn': (625, 838), 'back_btn': (728, 950), 'quit_to_main_btn': (1035, 608),
    'final_quit_btn': (960, 570)}
    memObj = MemoryManager(btn_location_dic=btn_loc_dictionary)
    print('Switch to ksp')
    time.sleep(4)
    memObj.restart_ksp()

        


