import pyautogui
import krpc
import time
import os
import subprocess


class MemoryManager:
    EXEC_PATH = '"C:\\Program Files (x86)\\Steam\\steamapps\\common\\Kerbal Space Program\\KSP_x64.exe"'


    def __init__(self, btn_location_dic=None):
        pyautogui.FAILSAFE = True

        if btn_location_dic is None:
            raise Exception('You must specify the locations of the buttons for exiting')

        self.QUIT_BTN_LOCATION = btn_location_dic['quit_btn']
        self.BACK_BTN_LOCATION = btn_location_dic['back_btn']
        self.FINAL_QUIT_BTN = btn_location_dic['final_quit_btn']
        self.START_BTN = btn_location_dic['start_btn']
        self.RESUME_BTN = btn_location_dic['resume_btn']
        self.SAVE_GAME_BTN = btn_location_dic['save_game_btn']
        self.QUIT_TO_MAIN_BTN_LOCATION = btn_location_dic['quit_to_main_btn']

    def restart_ksp(self):
        pyautogui.PAUSE = .75
        print('Quitting to Main Menu')
        pyautogui.press('esc')


        x, y = self.QUIT_TO_MAIN_BTN_LOCATION
        print(f"moving cursor to x: {x}, y: {y}")
        pyautogui.moveTo(x, y)
        pyautogui.PAUSE = 4
        pyautogui.click()

        print('Exiting')
        pyautogui.PAUSE = 4
        x, y = self.BACK_BTN_LOCATION
        print(f"moving cursor to x: {x}, y: {y}")
        pyautogui.moveTo(x, y)
        pyautogui.PAUSE = 4
        pyautogui.click()

        x, y = self.QUIT_BTN_LOCATION
        print(f"moving cursor to x: {x}, y: {y}")
        pyautogui.moveTo(x, y)
        pyautogui.PAUSE = 4
        pyautogui.click()

        x, y = self.FINAL_QUIT_BTN
        print(f"moving cursor to x: {x}, y: {y}")
        pyautogui.moveTo(x, y)
        pyautogui.PAUSE = 4
        pyautogui.click()

        subprocess.Popen(self.EXEC_PATH)
        time.sleep(60)

        print('Starting the game')
        x, y = self.START_BTN
        print(f"moving cursor to x: {x}, y: {y}")
        pyautogui.moveTo(x, y)
        pyautogui.PAUSE = 4
        pyautogui.click()

        x,y = self.RESUME_BTN
        print(f"moving cursor to x: {x}, y: {y}")
        pyautogui.moveTo(x, y)
        pyautogui.PAUSE = 4
        pyautogui.click()

        x, y = self.SAVE_GAME_BTN
        print(f"moving cursor to x: {x}, y: {y}")
        pyautogui.moveTo(x, y)
        pyautogui.PAUSE = 4
        pyautogui.click(x, y)
        pyautogui.click(x, y)

        print('Sequence Finished')

if __name__ == "__main__":
    print("other coordinate system")
    btn_loc_dictionary = {'quit_btn': (625, 838), 'back_btn': (728, 950), 'quit_to_main_btn': (1035, 608),
                          'final_quit_btn': (960, 570)}
    memObj = MemoryManager(btn_location_dic=btn_loc_dictionary)
    print('Switch to ksp')
    time.sleep(4)
    memObj.restart_ksp()
