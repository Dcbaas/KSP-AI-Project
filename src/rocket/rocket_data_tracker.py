import krpc
import numpy as np
import numpy.linalg as la
import time
import math
from typing import List


class RocketData:
    def __init__(self, connection):
        self.connection = connection
        self.vessel = self.connection.space_center.active_vessel
        self.start_time = time.time()  # I get the initial time of the program in order to keep track of duration

        self.situation = self.connection.add_stream(getattr, self.vessel, 'situation')
        self.orbit = self.connection.add_stream(getattr, self.vessel, 'orbit')
        self.parts_list = [(p.name, p.decouple_stage) for p in self.vessel.parts.all]
        self.stage = max(p.decouple_stage for p in self.vessel.parts.all)
        self.direction = self.connection.add_stream(self.vessel.direction, self.vessel.surface_reference_frame)

        """
        Inputs
        pitch, heading, roll, throttle, fuel remaining, all orbit stats, velocity, dynamic pressure
        """
        self.flight = self.connection.add_stream(self.vessel.flight, self.orbit().body.reference_frame)
        self.throttle = self.connection.add_stream(getattr, self.vessel.control, 'throttle')
        self.liquid_fuel = self.connection.add_stream(self.vessel.resources.amount, 'LiquidFuel')
        self.oxidizer = self.connection.add_stream(self.vessel.resources.amount, 'Oxidizer')

    def get_inputs(self):
        flight_snapshot = self.flight()
        orbit_snapshot = self.orbit()


        inputs = [flight_snapshot.heading / 360, flight_snapshot.pitch / 90, flight_snapshot.roll / 360, flight_snapshot.speed / 2000,
                  flight_snapshot.horizontal_speed / 500, flight_snapshot.vertical_speed / 500, self.throttle(),
                  min(self.liquid_fuel(), self.oxidizer())/100, orbit_snapshot.apoapsis_altitude / 100000,
                  orbit_snapshot.periapsis_altitude /100000, orbit_snapshot.inclination, orbit_snapshot.eccentricity,
                  flight_snapshot.dynamic_pressure / 1000]
        return inputs

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

    def get_remaining_fuel(self):
        return min(self.liquid_fuel, self.oxidizer)

    def is_valid_flight(self) -> bool:
        flight_snapshot = self.flight()
        orbit_snapshot = self.orbit()
        direction_snapshot = np.array(self.direction())

        # zero altitude after x time condition
        if self.vessel.met > 10 and flight_snapshot.speed == 0:
            print('Rocket never left')
            return False

        # vessel not in ocean condition
        if self.vessel.met > 10 and (self.situation() == self.situation().docked
                or self.situation() == self.situation().landed
                or self.situation() == self.situation().splashed):
            print('Rocket not flying anymore')
            return False

        # zero fuel condition
        if min(self.liquid_fuel(), self.oxidizer()) == 0:
            print('Rocket out of fuel')
            return False

        # If rocket is ballistic. As in flying towards the ground
        horizontal_direction = np.array((0, direction_snapshot[1], direction_snapshot[2]))
        pitch = self.angle_between_vectors(direction_snapshot, horizontal_direction)
        if direction_snapshot[0] < 0:
            pitch = -pitch
        # To Santiago. We can't have the failure condition be at 0. We need a tolerance to allow it to fly at 0
        if pitch < -3 and flight_snapshot.mean_altitude < 70000:
            print(f'Went Ballistic with pitch{pitch} at altitude {flight_snapshot.mean_altitude}')
            return False

        return True

    def get_closest_approach(self):
        return self.mun_target.orbit.distance_at_closest_approach(self.orbit())

    def get_horizontal_speed(self):
        flight_snapshot = self.flight()
        return flight_snapshot.horizontal_speed

    def angle_between_vectors(self, u, v):
        """
        Get the angle between two vectors. Used to get the
        pitch of the ship. Code was written by David Wolever.
        It was the best solution we found. Better than anything else we could think of.
        :param u:
        :param v:
        :return:
        """
        vec1_unit = self.get_unit_vector(u)
        vec2_unit = self.get_unit_vector(v)
        return np.arccos(np.clip(np.dot(vec1_unit, vec2_unit), -1.0, 1.0)) * (180/math.pi)

    def get_unit_vector(self, vector):
        """
        Gets the unit vector of a single direction vector.
        Part of getting the angle between vectors. This code came from a stack overflow user David Wolever
        This solution was better then anything else we could dream up.
        https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python
        :param vector:
        :return:
        """
        return vector / la.norm(vector)
