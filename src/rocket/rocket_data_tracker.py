import krpc
import numpy as np
import numpy.linalg as la
import time 
from typing import List
class RocketData:

    def __init__(self, connection):
        DEST_LOC = np.array((-0.49409718944856473, 59.473877823389955))
        self.connection = connection
        self.mun_target = connection.space_center.bodies['Mun']
        self.connection.space_center.target_body = self.mun_target #what is this line of code doing ?
        self.vessel = connection.space_center.active_vessel
        self.start_time = time.time() # I get the initial time of the program in order to keep track of duration


        self.position = connection.add_stream(vessel.position, self.mun_target.reference_frame)
        self.CARTESIAN_POS = np.array(self.mun_target.surface_position(DEST_LOC[0], DEST_LOC[1], self.mun_target.reference_frame))

        self.situation = connection.add_stream(vessel.situation)
        self.orbit = connection.add_stream(vessel.orbit)

    def get_distance(self):
        basis_dist = self.CARTESIAN_POS - np.array(self.position())
        return la.norm(basis_dist)

    def get_situation(self):
        # Isn't this situation the one retrieved from the vesel ?
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
        return np.array((orbit.body, orbit.apoapsis_altitude, orbit.periapsis_altitude))

    def getResourcesAmount(self, vessel) -> List[float]:
        return [self.vessel.resourses.amount["LiquidFuel"], self.vessel.resourses.amount["Oxidizer"], self.vessel.resourses.amount["ElectricCharge"]]

    def getSituation(self) -> krpc.VesselSituatuion:
        return self.vessel.situation


    @property
    def asses_fligh(self) -> bool:
      # zero altitude after x time condition
      if (self.vessel.met > 10 and vessel.situation == VesselSituatuion.pre_launch):
          return False

      # vesel not in ocean condition 
      if (self.vessel.situation == krpc.VesselSituatuion.docked 
              and self.vessel.situation == krpc.VesselSituatuion.landed 
              and self.vessel.situation == krpc.VesselSituatuion.splashed):
          return False  

      # zero fuel condition
      # Insuficient electric power
      if (self.vessel.resourses.amount["LiquidFuel"] == 0 
              or self.vessel.resourses.amount["Oxidizer"] == 0):
          return False

      # zero electric charge condition
