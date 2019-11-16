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

        # Needed for calculating distance from Mun before being in Mun's sphere of influence. 
        self.position = connection.add_stream(vessel.position, self.mun_target.reference_frame)
        self.CARTESIAN_POS = np.array(self.mun_target.surface_position(DEST_LOC[0], DEST_LOC[1], self.mun_target.reference_frame))

    def get_distance(self):
        basis_dist = self.CARTESIAN_POS - np.array(self.position())
        return la.norm(basis_dist)


