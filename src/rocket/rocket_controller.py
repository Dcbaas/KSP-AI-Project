import krpc


class RocketController:
    """
    Controls the rockets actual flight.
    :param vessel - The vessel object representing the rocket in KSP
    :var control - The control object for the vessel. This controls the throttle, roll, and landing gear primarily but also '
    can control all other functions of the ship. DON'T USE FOR SHIP CONTROL
    :param auto_pilot - The autopilot object of the vessel. This is the primary means for controlling the direction the
    rocket will be going.

    """
    def __init__(self, vessel):
        """
        Initializes the RocketController. Sets certian fields to ensure the autopilot works correctly
        :param vessel: the vessel object that this RocketController will control
        """
        self.vessel = vessel
        self.control = vessel.control
        self.auto_pilot = vessel.auto_pilot

        self.control.sas = False
        self.control.rcs = False

        self.auto_pilot.engage()

    def update_controls(self, pitch, heading, roll, throttle, sas=False, rcs=False, landing_gear=False):
        """
        TODO: Implement comments
        :param pitch:
        :param heading:
        :param roll:
        :param throttle:
        :param sas:
        :param rcs:
        :param landing_gear:
        :return:
        """
        self.auto_pilot.target_pitch_and_heading(pitch, heading)
        self.control.roll = roll
        self.control.throttle = throttle
        self.control.legs = landing_gear
        self.control.sas = sas
        self.control.rcs = rcs

    def stage_rocket(self):
        """
        TODO implement comments
        :return:
        """
        self.control.activate_next_stage()


