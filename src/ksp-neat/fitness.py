import time

import krpc
import neat

from game_controller import GameController
from rocket import RocketController
from stats_monitor import Monitor
from rocket_data_tracker import RocketData
from MemoryManager import MemoryManager

EIGHTH_VALUE = 250000
QUARTER_VALUE = 500000
START_POINTS = 2000000
TARGET_CLOSEST_APPROACH = 500000
DISTANCE_TOLERANCE = 1000
TARGET_SPEED = 0.5

btn_mapping_dic = { 'quit_btn': (1665, 1339), 'back_btn': (1720, 1435), 'final_quit_btn': (1916, 1022),
                    'start_btn': (1665, 1075), 'resume_btn': (1705, 1018),
                    'save_game_btn': (1899, 909), 'quit_to_main_btn': (2103, 1168)}

def update_monitor(rocket_data, monitor):
    orbit_data = rocket_data.get_orbit_data()
    monitor.set_max_horizontal_speed(rocket_data.get_horizontal_speed())
    monitor.set_max_pe(orbit_data[1])
    monitor.set_max_ap(orbit_data[0])
    monitor.set_best_inclination(orbit_data[2])
    monitor.set_best_eccentricity(orbit_data[3])


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


def score_horizontal_speed(speed):
    if speed > 2000:
        return 2000
    return speed


def calc_fitness(monitor: Monitor):
    """
    """
    score = score_horizontal_speed(monitor.max_horizontal_speed) + score_altitude(monitor.max_ap) + score_altitude(
        monitor.max_pe) + score_inclination(
        monitor.best_inclination) + \
            score_eccentricity(monitor.best_eccentricity)

    return score


def still_valid():
    return True


def eval_genomes(genomes, config):
    """Executes genome actions and sets their resulting fitness"""
    RESTART_LIMIT = 100
    current_restarts = 0
    connection = krpc.connect(name='ai_server')

    mem_manager = MemoryManager(btn_location_dic=btn_mapping_dic)

    for genome_id, genome in genomes:
        connection.space_center.load("SHgame")
        time.sleep(5)
        current_restarts = current_restarts + 1
       # if current_restarts == RESTART_LIMIT:
           # Reset game
         #   connection.close()
        #    mem_manager.restart_ksp()
         #   connection = krpc.connect(name='distance_test')
          #  game_controller.restart()
           # current_restarts = 0

        # recurrent nn allows us to go back to previous decisions and iterate
        net = neat.nn.RecurrentNetwork.create(genome, config)

        # connection.space_center.load("SHgame")
        # time.sleep(5)

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
