import krpc
import sys


class Monitor:
    """
    When Tanner Gibson and his group ran his orbit AI for ksp he has a monitor track the max values
    of certain statistics so that he didn't have to run the fitness calculation live
    With that in mind we are doing something similar here.
    """
    def __init__(self):
        """
        Initialize the monitor. For our rockets fitness score we tracked the values listed below.
        """
        # While launching from Kerbin
        self.max_ap = 0
        self.max_pe = 0
        self.best_eccentricity = sys.maxsize
        self.best_inclination = sys.maxsize
        self.max_horizontal_speed = 0


        # TODO maybe we want to be able to load previous data from file in case of crash
        self.final_situation = None

    def set_max_ap(self, ap) -> None:
        """
        Sets the maxinum apoapsis the rocket reaches.
        :param ap: The apoapsis value that wants to be the maximum value
        :return: None
        """
        if ap > self.max_ap:
            self.max_ap = ap

    def set_max_pe(self, pe) -> None:
        """
        Sets the maximum periapsis value the rocket reaches
        :param pe: The periapsis value that wants to be the maximum value
        :return: None
        """
        if pe > self.max_pe:
            self.max_pe = pe

    def set_best_eccentricity(self, eccentricity) -> None:
        """
        Set the value of the eccentricity. Values are accepted if they are lower then the
        current value of the eccentricity.
        :param eccentricity: The new eccentricity value.
        :return: None
        """
        if eccentricity < self.best_eccentricity:
            self.best_eccentricity = eccentricity

    def set_best_inclination(self, inclination) -> None:
        """
        Set the value of the inclination. Values are accepted if they are lower then the
        current value of the inclination.
        :param inclination: The new inclination value.
        :return: None
        """
        if inclination < self.best_inclination:
            self.best_inclination = inclination

    def set_final_situation(self, situation):
        """
        DEPRICATED
        Monitors the final situation the rocket was in. When our goal was to get to the Mun there was differnet scoring based
        on what our final situation was. We thought there was a possiblity to use it for the orbit challange but no use
        was found
        :param situation: The new situation value being passed in.
        :return: None
        """
        self.final_situation = situation

    def set_max_horizontal_speed(self, speed):
        """
        Sets the max horizontal speed the rocket achived.
        :param speed: The horizontal speed of the rocket
        :return: None
        """
        if speed > self.max_horizontal_speed:
            self.max_horizontal_speed = speed