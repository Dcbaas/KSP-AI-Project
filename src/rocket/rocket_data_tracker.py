import krpc
import numpy as np
import numpy.linalg as la
import time
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
        inputs = [flight_snapshot.heading, flight_snapshot.pitch, flight_snapshot.roll, flight_snapshot.speed,
                  flight_snapshot.horizontal_speed, flight_snapshot.vertical_speed, self.throttle(),
                  min(self.liquid_fuel(), self.oxidizer()), orbit_snapshot.apoapsis_altitude,
                  orbit_snapshot.periapsis_altitude, orbit_snapshot.inclination, orbit_snapshot.eccentricity,
                  flight_snapshot.dynamic_pressure]
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
        print(flight_snapshot.pitch)
        print(self.vessel.control.pitch)
        if flight_snapshot.pitch < 0 and flight_snapshot.mean_altitude < 70000:
            print('Went Ballistic')
            return False

        return True

    def get_closest_approach(self):
        return self.mun_target.orbit.distance_at_closest_approach(self.orbit())

    def get_horizontal_speed(self):
        flight_snapshot = self.flight()
        return flight_snapshot.horizontal_speed
