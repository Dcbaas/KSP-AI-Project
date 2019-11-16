import krpc
import numpy as np
import numpy.linalg as la

class RocketData:
    def __init__(self, connection):
        self.connection = connection
        self.mun_target = connection.space_center.bodies['Mun']
        self.connection.space_center.target_body = self.mun_target
        vessel = connection.space_center.active_vessel
        # Needed for calculating distance from Mun before being in Mun's sphere of influence. 
        self.position = connection.add_stream(vessel.position, self.mun_target.reference_frame)


