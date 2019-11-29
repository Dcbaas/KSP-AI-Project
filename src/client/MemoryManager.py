import pyautogui
import krpc
import time
import os
import subprocess


class MemoryManager:
    """
    This class was supposed to be the memory manager for automattically closing and restarting Kerbal Space Program
    It was meant to allow us to start the simulation and just leave it alone while we waited for results.

    Unfortuantly When we went to implement the system on the target machine we encoutered problems with the mouse
    clicks not interacting with Kerbal Space Program properly. We didn't have time to troubleshoot the problem
    so an automatic restart function was abandoned.
    """
    EXEC_PATH = '"C:\\Program Files (x86)\\Steam\\steamapps\\common\\Kerbal Space Program\\KSP_x64.exe"'


    def __init__(self, btn_location_dic=None):
        """
        Initialized the memory managment object. The object was initialized with a dictionary contianing the x,y values
        for locations to click buttons within KSP.

        :param btn_location_dic: The locations on the screen where to click buttons in KSP.
        """
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
        """
        The method used to restart KSP. Went through all the mouse clicks to close down and restart KSP.
        For restarting the game itself we used the subprocess library to start a new ksp process. This allowed to
        avoid one more mouse click.
        :return: Void
        """
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
