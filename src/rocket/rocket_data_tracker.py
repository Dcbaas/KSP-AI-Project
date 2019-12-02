import krpc
import numpy as np
import numpy.linalg as la
import time
import math


class RocketData:
    """
    RocketData did live tracking of all the statistics. We used a separate class because
    It made sense to group all the objects needed for tracking the data in a location separate from
    the rocket controller. This class uses streams to get data while also keeping rpc bandwidth usage low.
    """
    def __init__(self, connection):
        """
        Initializes all the objects needed for tracking the rockets progress. All of critical data points needed
        are extracted from data streams to keep bandwidth usage lower during testing.

        :param connection: The connection to KSP being used to get the data.
        """
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
        """
        Gets the inputs for the neat algorithm and returns them in a list. All of the values are normalized to be the
        maximum value during launch.

        :return: A list containing the inputs used by the neat algorithm
        """
        flight_snapshot = self.flight()
        orbit_snapshot = self.orbit()


        inputs = [flight_snapshot.heading / 360, flight_snapshot.pitch / 90, flight_snapshot.roll / 360, flight_snapshot.speed / 2000,
                  flight_snapshot.horizontal_speed / 500, flight_snapshot.vertical_speed / 500, self.throttle(),
                  min(self.liquid_fuel(), self.oxidizer())/100, orbit_snapshot.apoapsis_altitude / 100000,
                  orbit_snapshot.periapsis_altitude /100000, orbit_snapshot.inclination, orbit_snapshot.eccentricity,
                  flight_snapshot.dynamic_pressure / 1000]
        return inputs

    def get_situation(self):
        """
        Gets the vessel's situation

        :return: The enum defining the vessels situation.
        """
        return self.situation()

    def get_orbit_data(self):
        """
        Returns orbit data related to the craft. The following values are returned as part of the orbit data

        apoapis_altitude
        periapsis_altitude
        inclination
        eccentricity

        :return: an np array with the fields above
        """
        orbit = self.orbit()

        return orbit.apoapsis_altitude, orbit.periapsis_altitude, orbit.inclination, orbit.eccentricity

    def get_remaining_fuel(self):
        """
        Gets the fuel currently remaning on the vessel.
        This only includes liquid based fuel and not SRB fuel

        :return: The amount of fuel remaining.
        """
        return min(self.liquid_fuel, self.oxidizer)

    def is_valid_flight(self) -> bool:
        """
        Checks if flight is still valid.
        Flight is still valid if none of the following conditions are true

        1. The rocket is standing still for longer than 10 seconds
        2. The rocket has not crashed or been partially destroyed.
        3. The rocket has not run out of fuel
        4. The rocket has not gone ballistic.

        :return: True if none of those conditions are met, false otherwise.
        """
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

        if pitch < -3 and flight_snapshot.mean_altitude < 70000:
            print(f'Went Ballistic with pitch{pitch} at altitude {flight_snapshot.mean_altitude}')
            return False

        return True

    def get_horizontal_speed(self):
        flight_snapshot = self.flight()
        return flight_snapshot.horizontal_speed

    def angle_between_vectors(self, u, v):
        """
        Get the angle between two vectors. Used to get the
        pitch of the ship during failure conditions. Code was written by David Wolever.
        It was the best solution we found. Better than anything else we could think of.
        https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python
        :param u: The starting vector for finding the angle
        :param v: The ending vector for finding the angle
        :return: The angle between the two vectors.
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
        :param vector: The vector being broken into a unit vector.
        :return: The vector represented as a unit vector.
        """
        return vector / la.norm(vector)
