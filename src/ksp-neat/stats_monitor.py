import krpc
import sys


class Monitor:
    """
    When nonprofitgibi ran his orbit AI for ksp he has a monitor track the max values
    of certain statistics so that he didn't have to run the fitness calculation live
    With that in mind we are doing something similar here.
    """
    def __init__(self):
        # While launching from Kerbin
        self.max_ap = 0
        self.max_pe = 0
        self.best_eccentricity = sys.maxsize
        self.best_inclination = sys.maxsize
        self.max_horizontal_speed = 0


        # TODO maybe we want to be able to load previous data from file in case of crash
        self.final_situation = None

    def set_max_ap(self, ap) -> None:
        if ap > self.max_ap:
            self.max_ap = ap

    def set_max_pe(self, pe) -> None:
        if pe > self.max_pe:
            self.max_pe = pe

    def set_best_eccentricity(self, eccentricity) -> None:
        if eccentricity < self.best_eccentricity:
            self.best_eccentricity = eccentricity

    def set_best_inclination(self, inclination) -> None:
        if inclination < self.best_inclination:
            self.best_inclination = inclination

    def set_final_situation(self, situation):
        self.final_situation = situation

    def set_max_horizontal_speed(self, speed):
        if speed > self.max_horizontal_speed:
            self.max_horizontal_speed = speed