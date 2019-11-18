"""
LET'S DO THE TIME WARP AGAIN!
https://www.youtube.com/watch?v=ZanHo6Wn1H4
"""

class TimeWarpHelper:
    WARP_FACTOR_LIMIT = 5
    def __init__(self, connection):
        self.connection = connection

    def warp_till_body_shift(self):
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
