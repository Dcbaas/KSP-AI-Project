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


def update_monitor(rocket_data, monitor):
    """
    Updates the values in a Monitor object. These values at failure or success
    will be used to calculate the fitness score.

    :param rocket_data: The rocket data instance we are gettting information from.
    :param monitor: The monitor object being used to store the data.
    :return: void
    """
    orbit_data = rocket_data.get_orbit_data()
    monitor.set_max_horizontal_speed(rocket_data.get_horizontal_speed())
    monitor.set_max_pe(orbit_data[1])
    monitor.set_max_ap(orbit_data[0])
    monitor.set_best_inclination(orbit_data[2])
    monitor.set_best_eccentricity(orbit_data[3])


def score_altitude(altitude):
    """
    Score the altitude. The goal is to reach but not surpass the target altitude.
    :param altitude: The altitude being measured
    :return: The value of altitude if below or at target. the target altitude minus the height beyond it if
    past the target.
    """
    TARGET_ALT = 100000
    if altitude > TARGET_ALT:
        return TARGET_ALT - (altitude - TARGET_ALT)
    return altitude


def score_inclination(inclination):
    """
    Score the inclination of the rockets run. If the rocket reaches inclination of 0, then 1500 is returned as the score
    Otherwise the score is 1/inclination value.
    :param inclination: The inclination at failure.
    :return: 1500 if score is 0, 1 / inclination otherwise.
    """
    if inclination < 0.001:
        return 1500
    return 1 / inclination


def score_eccentricity(eccentricity):
    """
    Score the eccentricity of the rockets orbit (the roundness of the orbit).
    :param eccentricity: The eccentricity value of the orbit at failure.
    :return: 1500 if the eccentricity is essentially 0. 1 / eccentricity otherwise.
    """
    if eccentricity < 0.001:
        return 1500
    return 1 / eccentricity


def score_horizontal_speed(speed):
    """
    Score the horizontal speed of the rocket at failure. The ideal final horizontal speed at the end should be around
    2000 m/s
    :param speed: The horizontal speed of the rocket.
    :return: the value of the horizontal speed at failure with the max value being 2000
    """
    if speed > 2000:
        return 2000
    return speed


def calc_fitness(monitor: Monitor):
    """
    Score the fitness of a rockets run. The score is the horizontal speed + the altitude of the apoapsis +
    the altitude of the periapsis + the inclination score + the eccentricity score

    :param monitor: The monitor that has the values for the fitness score
    :return: The final fitness score for a genomes run. The max score is 205000
    """
    score = score_horizontal_speed(monitor.max_horizontal_speed) + score_altitude(monitor.max_ap) + score_altitude(
        monitor.max_pe) + score_inclination(
        monitor.best_inclination) + \
            score_eccentricity(monitor.best_eccentricity)

    return score

def eval_genomes(genomes, config):
    """
    Executes genome actions and sets their resulting fitness. This is the main driver of the AI program.
    This section is where the rocket is flown and at failure the genome is evaluated.

    :param genomes: The genomes being run for this simulation
    :param config: The config file that sets the parameters for this simulation
    :return: None
    """
    connection = krpc.connect(name='distance_test')
    for genome_id, genome in genomes:
        # recurrent nn allows us to go back to previous decisions and iterate
        net = neat.nn.RecurrentNetwork.create(genome, config)
        connection.space_center.load("SHgame")
        time.sleep(5)

        rocket_data = RocketData(connection)
        rocket_controller = RocketController(connection.space_center.active_vessel)
        game_controller = GameController(connection, rocket_controller)
        monitor = Monitor()

        game_controller.launch(rocket_data)  # prepare to fly
        start = time.time()
        elapsed = 0
        while elapsed < 1200 and rocket_data.is_valid_flight():
            #  fly ship!
            rocket_controller.update_controls(net.activate(rocket_data.get_inputs()), rocket_data)
            update_monitor(rocket_data, monitor)
            elapsed = time.time() - start
        score = calc_fitness(monitor)
        print(score)
        genome.fitness = score
