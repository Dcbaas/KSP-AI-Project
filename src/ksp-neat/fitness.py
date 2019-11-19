import time

import krpc
import neat

from game_controller import GameController
from rocket import RocketController
from stats_monitor import Monitor
from rocket_data_tracker import RocketData

EIGHTH_VALUE = 250000
QUARTER_VALUE = 500000
START_POINTS = 2000000
TARGET_CLOSEST_APPROACH = 500000
DISTANCE_TOLERANCE = 1000
TARGET_SPEED = 0.5


def score_altitude(altitude):
    """
    Score the altitude. The goal is to reach but not surpass the target altitude.
    :param altitude: The altitude being
    measured
    :return: The value of altitude if below or at target. the target altitude minus the height beyond it if
    past the target.
    """
    TARGET_ALT = 100000
    if altitude > TARGET_ALT:
        return TARGET_ALT - (altitude - TARGET_ALT)
    return altitude


def score_inclination(inclination):
    if inclination < 0.001:
        return 1500
    return 1 / inclination


def score_eccentricity(eccentricity):
    if eccentricity < 0.001:
        return 1500
    return 1 / eccentricity


def calc_fitness(monitor: Monitor):
    """
    """
    score = score_altitude(monitor.max_ap) + score_altitude(monitor.max_pe) + score_inclination(
        monitor.best_inclination) + \
            score_eccentricity(monitor.best_eccentricity)

    return score


def still_valid():
    return True


def eval_genomes(genomes, config):
    """Executes genome actions and sets their resulting fitness"""
    connection = krpc.connect(name='distance_test')
    rocket_data = RocketData(connection)
    rocket_controller = RocketController(connection.space_center.active_vessel)
    game_controller = GameController(connection, rocket_controller)
    for genome_id, genome in genomes:
        # recurrent nn allows us to go back to previous decisions and iterate
        net = neat.nn.RecurrentNetwork.create(genome, config)
        game_controller.restart()  # load game
        monitor = Monitor()
        monitor.set_final_situation(rocket_controller.vessel.situation)
        time.sleep(10)  # TODO: determine time for game to load
        game_controller.launch(rocket_data)  # prepare to fly
        start = time.time()
        elapsed = 0
        while elapsed < 60 and still_valid():  # TODO: add failure condition, set time correctly (currently 60 secs)
            #  fly ship!
            rocket_controller.update_controls(net.activate(rocket_data.get_inputs()), rocket_data)
            elapsed = time.time() - start
        genome.fitness = calc_fitness(monitor)
