import krpc
from rocket_data_tracker import RocketData


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
        Initializes the RocketController. Sets certain fields to ensure the autopilot works correctly
        :param vessel: the vessel object that this RocketController will control
        """
        self.vessel = vessel
        self.control = vessel.control
        self.auto_pilot = vessel.auto_pilot

        self.control.sas = False
        self.control.rcs = False

        self.auto_pilot.engage()

    def update_controls(self, outputs, rocket_data):
        """
        This function is based off of the implementation by nonprofitgibi
        https://github.com/nonprofitgibi/PythonLearnsKSP/blob/master/GeneticAlgorithm/ksp.py
        Updates the controls to change how the ship is flying.
        :param rocket_data: The rocket data that will be updated if a stage occurs.
        :param outputs: the list of outputs from the activation function.
        :return: None
        """
        heading = outputs[0] * 360
        pitch = outputs[1] - 0.5 * 180
        throttle = outputs[2]
        # print(throttle)
        self.auto_pilot.target_pitch_and_heading(pitch, heading)
        self.control.throttle = throttle
        if outputs[3] > 0.5:
            self.stage_rocket(rocket_data)
    def stage_rocket(self, rocket_data:RocketData):
        """
        TODO implement comments
        :return:
        """
        self.control.activate_next_stage()
        rocket_data.stage -= 1

    def set_throttle(self, throttle):
        self.control.throttle = throttle


