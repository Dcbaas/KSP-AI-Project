import krpc
import numpy as np
import numpy.linalg as la

class RocketData:

    def __init__(self, connection):
        DEST_LOC = np.array((-0.49409718944856473, 59.473877823389955))
        self.connection = connection
        self.mun_target = connection.space_center.bodies['Mun']
        self.connection.space_center.target_body = self.mun_target
        vessel = connection.space_center.active_vessel
        flight = vessel.flight(vessel.orbit.body.reference_frame)

        self.speed = connection.add_stream(getattr, flight, 'speed')

        self.position = connection.add_stream(vessel.position, self.mun_target.reference_frame)
        self.CARTESIAN_POS = np.array(self.mun_target.surface_position(DEST_LOC[0], DEST_LOC[1], self.mun_target.reference_frame))
        self.situation = connection.add_stream(getattr, vessel, 'situation')
        self.orbit = connection.add_stream( getattr, vessel, 'orbit')

    def get_distance(self):
        basis_dist = self.CARTESIAN_POS - np.array(self.position())
        return la.norm(basis_dist)

    def get_speed(self):
        return self.speed()

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
        return orbit.body.name, orbit.apoapsis_altitude, orbit.periapsis_altitude

    def get_closest_approach(self):
        return self.mun_target.orbit.distance_at_closest_approach(self.orbit())
