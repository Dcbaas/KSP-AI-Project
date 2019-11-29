"""
LET'S DO THE TIME WARP AGAIN!
https://www.youtube.com/watch?v=ZanHo6Wn1H4
"""

class TimeWarpHelper:
    """
    Our original goal was to get a rocket to the Mun. In order to do that we needed to manipulate the warp tool that
    is provided by KSP. We would fly towards the Mun and then warp closer and then contiue with our simulation
    """
    WARP_FACTOR_LIMIT = 5
    def __init__(self, connection):
        """
        initialize the warp helper. The warp helper need a connection to KSP.
        :param connection: The connection to KSP
        """
        self.connection = connection

    def warp_till_body_shift(self):
        """
        Warps the rocket towards the Mun. The trigger for exiting the warp helper was a when the rocket left the
        sphere of influence of Kerbin.
        :return: void 
        """
        space_center = self.connection.space_center
        vessel_orbit = space_center.active_vessel.orbit
        if not space_center.can_rails_warp_at(1):
            raise Exception(
                'You didn\'t secure the ship before trying to warp. Stop the ship from accelerating and try again')
        current_warp_factor = 1
        space_center.rails_warp_factor = current_warp_factor
        while vessel_orbit.body.name == 'Kerbin':
            if current_warp_factor == self.WARP_FACTOR_LIMIT:
                pass
            elif space_center.can_rails_warp_at(current_warp_factor + 1):
                current_warp_factor = current_warp_factor + 1
                space_center.rails_warp_factor = current_warp_factor
        space_center.rails_warp_factor = 0
