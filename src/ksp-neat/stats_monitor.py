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

        # While performing transfer
        self.closest_approach = sys.maxsize

        # While landing at Mun
        self.closest_landing_dist = sys.maxsize
        self.lowest_speed_at_touchdown = sys.maxsize
        # TODO maybe we want to be able to load previous data from file in case of crash
        self.final_situation = None

    def set_max_ap(self, ap:int) -> None:
        if ap > self.max_ap:
            self.max_ap = ap

    def set_max_pe(self, pe:int) -> None:
        if pe > self.max_pe:
            self.max_pe = pe

    def set_closest_approach(self, dist) -> None:
        if dist < self.closest_approach:
            self.closest_approach = dist

    def set_closest_landing_dist(self, dist) -> None:
        if dist < self.closest_landing_dist:
            self.closest_landing_dist = dist

    def set_lowest_speed_at_touchdown(self, speed, body) -> None:
        if body.name is 'Mun' and speed < self.lowest_speed_at_touchdown:
            self.lowest_speed_at_touchdown = speed

    def set_final_situation(self, situation):
        self.final_situation = situation