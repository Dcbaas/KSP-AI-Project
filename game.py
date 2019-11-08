"""
This module sets up KSP to work with code across a kRPC server
"""
import krpc


class Game:
    """
    Defines all variables and methods related to connecting
    this codebase to KSP kRPC server

    :var self.conn The connection instance to a kRPC server
    :var self.kerbin The character instance in KSP
    :var self.vessel The ship currently prepared to launch
    """

    def hasFailed(self) -> bool:
        """Defines situations for a failed launch"""
        if not self.vessel.situation.pre_launch and self.vessel.speed == 0:  # vessel has stopped
            return True
        if self.vessel.flight().pitch == -90:  # vessel is going towards Earth
            return True
        if self.vessel.situation not in [  # vessel should not be swimming
            self.vessel.situation.flying,
            self.vessel.situation.orbiting,
            self.vessel.situation.sub_orbital
        ]:
            return True
        if min([self.vessel.resources.amount("LiquidFuel"),
                self.vessel.resources.amount("Oxidizer")]) == 0:  # out of fuel
            return True
        return False

    def launch(self):
        """
        Tutorial code for launching a rocket:
        https://krpc.github.io/krpc/tutorials/launch-into-orbit.html
        """
        turn_start_altitude = 250
        turn_end_altitude = 45000
        target_altitude = 150000

        # Set up streams for telemetry
        ut = self.conn.add_stream(getattr, self.conn.space_center, 'ut')
        altitude = self.conn.add_stream(getattr, self.vessel.flight(), 'mean_altitude')
        apoapsis = self.conn.add_stream(getattr, self.vessel.orbit, 'apoapsis_altitude')
        stage_2_resources = self.vessel.resources_in_decouple_stage(stage=2, cumulative=False)
        srb_fuel = self.conn.add_stream(stage_2_resources.amount, 'SolidFuel')

        # Pre-launch setup
        self.vessel.control.sas = False
        self.vessel.control.rcs = False
        self.vessel.control.throttle = 1.0

        # Activate the first stage
        self.vessel.control.activate_next_stage()
        self.vessel.auto_pilot.engage()
        self.vessel.auto_pilot.target_pitch_and_heading(90, 90)

        # Main ascent loop
        srbs_separated = False
        turn_angle = 0
        while True:

            # Gravity turn
            if turn_start_altitude < altitude() < turn_end_altitude:
                frac = ((altitude() - turn_start_altitude) /
                        (turn_end_altitude - turn_start_altitude))
                new_turn_angle = frac * 90
                if abs(new_turn_angle - turn_angle) > 0.5:
                    turn_angle = new_turn_angle
                    self.vessel.auto_pilot.target_pitch_and_heading(90 - turn_angle, 90)

            # Separate SRBs when finished
            if not srbs_separated:
                if srb_fuel() < 0.1:
                    self.vessel.control.activate_next_stage()
                    srbs_separated = True
                    print('SRBs separated')

            # Decrease throttle when approaching target apoapsis
            if apoapsis() > target_altitude * 0.9:
                print('Approaching target apoapsis')
                break

    def __init__(self):
        """Connect to KSP kRPC server"""
        self.conn = krpc.connect(name="SnakeHaterz")
        print(self.conn.getStatus())
        self.kerbin = self.conn.space_center.bodies["Kerbin"]
        self.vessel = self.conn.space_center.active_vessel
