import krpc
import numpy as np
import numpy.linalg as la
import time
from typing import List


class RocketData:
    def __init__(self, connection):
        self.connection = connection
        self.vessel = connection.space_center.active_vessel
        self.start_time = time.time()  # I get the initial time of the program in order to keep track of duration

        self.situation = connection.add_stream(getattr, self.vessel, 'situation')
        self.orbit = connection.add_stream(getattr, self.vessel, 'orbit')
        self.parts_list = [(p.name, p.decouple_stage) for p in self.vessel.parts.all]
        self.stage = max(p.decouple_stage for p in self.vessel.parts.all)


    def get_situation(self):
        return self.situation()

    def get_orbit_data(self):
        """
        Returns orbit data related to the craft. The following values are returned as part of the orbit data

        apoapis_altitude
        periapsis_altitude
        The body being orbited.

        :return: an np array with the fields above
        """
        orbit = self.orbit()

        return orbit.apoapsis_altitude, orbit.periapsis_altitude, orbit.inclination, orbit.eccentricity

    def getResourcesAmount(self):
        return [self.vessel.resourses.amount["LiquidFuel"], self.vessel.resourses.amount["Oxidizer"],
                self.vessel.resourses.amount["ElectricCharge"]]

    def getSituation(self):
        return self.vessel.situation

    def is_valid_flight(self) -> bool:
        # zero altitude after x time condition
        if self.vessel.met > 10 and self.situation() == self.situation().pre_launch:
            return False

        # vessel not in ocean condition
        if (self.situation() == self.situation().docked
                and self.situation() == self.situation().landed
                and self.situation() == self.situation().splashed):
            return False

        # zero fuel condition
        if (self.vessel.resourses.amount["LiquidFuel"] == 0
                or self.vessel.resourses.amount["Oxidizer"] == 0):
            return False

        return True

    def get_closest_approach(self):
        return self.mun_target.orbit.distance_at_closest_approach(self.orbit())
