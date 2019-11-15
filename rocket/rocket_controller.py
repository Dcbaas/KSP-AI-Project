import krpc


class RocketController:
    def __init__(self, vessel):
        self.vessel = vessel
        self.control = vessel.control
        self.auto_pilot = vessel.auto_pilot

        self.control.sas = False
        self.control.rcs = False

        self.auto_pilot.engage()

    def update_controls(self, pitch, heading, roll, throttle, sas=False, rcs=False, landing_gear=False):
        self.auto_pilot.target_pitch_and_heading(pitch, heading)
        self.control.roll = roll
        self.control.throttle = throttle
        self.control.legs = landing_gear
        self.control.sas = sas
        self.control.rcs = rcs

    def stage_rocket(self):
        self.control.activate_next_stage()


