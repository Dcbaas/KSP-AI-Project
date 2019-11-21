#TODO: add import statements
from rocket_data_tracker import RocketData
"""This should provide functionality for game functions/setup. Everything dealing indirectly with the rocket."""


class GameController:
    """
    Contains all functions related to setting up the game for handling launching and managing connections
    """

    def __init__(self, connection, rocket_controller):
        self.connection = connection
        self.rocket_controller = rocket_controller

    def restart(self):
        """Reload game (name is SHgame)"""
        self.connection.space_center.load("SHgame")
        # do we have to recreate rocket controller?
        # self.rocket_controller.update_controls(
        #     self.rocket_controller.control.pitch,
        #     self.rocket_controller.vessel.flight().heading,
        #     self.rocket_controller.control.roll,
        #     self.rocket_controller.control.throttle,
        # )
        # self.rocket_controller.set_throttle(1.0)

    def launch(self, rocket_data:RocketData):
        """Set up launch for AI"""
        self.connection.space_center.save("SHgame")  # will save game as SHgame.sfs
        self.rocket_controller.stage_rocket(rocket_data)
