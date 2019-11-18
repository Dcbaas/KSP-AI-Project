import time

import krpc
import neat

from game_controller import GameController
from rocket import RocketController
from stats_monitor import Monitor

EIGHTH_VALUE = 250000
QUARTER_VALUE = 500000
START_POINTS = 2000000
TARGET_CLOSEST_APPROACH = 500000
DISTANCE_TOLERANCE = 1000
TARGET_SPEED = 0.5


def is_stable_orbit(monitor):
    STABLE_HEIGHT = 70000
    return monitor.max_ap > STABLE_HEIGHT and monitor.max_pe > STABLE_HEIGHT

def calculate_orbit_decrement(height_val):
    TARGET_ORBIT_HEIGHT = 710000
    if height_val > TARGET_ORBIT_HEIGHT:
        return QUARTER_VALUE
    return QUARTER_VALUE * 1 / (TARGET_ORBIT_HEIGHT - height_val)


def calculate_closest_approach_decrement(approach_val):
    TARGET_CLOSEST_APPROACH = 500000
    if approach_val < TARGET_CLOSEST_APPROACH:
        return QUARTER_VALUE
    return QUARTER_VALUE * 1 / (approach_val - TARGET_CLOSEST_APPROACH)


def calc_fitness(monitor : Monitor):
    """
    The goal for the rockets is to get to a fitness value of zero.
    We start from 2,000,000 as a fitness score
    Fitness is calculated in four stages'

    1. Pre orbit of Kerbin. We want to reward getting to orbit first before flying towards the Mun
    Therefore we deduct points for advancing towards orbit.

    2. If the situation recorded is orbit then we calculate if it is a valid orbit. 100km orbit will be ideal so
    The closer to that target the rocket gets. the more points that will be deducted. These first two steps can bring
    the score down to a minimum of 1,000,000 points.

    3. Hohmann transfer to the Mun: The AI will get more points deducted for getting a closest approach to the Mun

    4. Landing on the Mun. Points are deducted for being as close to the designated landing target as possible. Points
    are also deducted for landing at a safe velocity. 250,000 points are determined by the landing accuracy and the
    final 250,000 points are determine by final landing speed.
    """
    START_POINTS = 2000000
    TARGET_ORBIT_HEIGHT = 710000
    TARGET_CLOSEST_APPROACH = 500000
    # Pre Orbit
    if monitor.final_situation is monitor.final_situation.flying or \
        monitor.final_situation is monitor.final_situation.sub_orbital:
        score = START_POINTS - (500000 * 1/(TARGET_ORBIT_HEIGHT - monitor.max_ap))
    # Getting to orbit
    elif monitor.final_situation is monitor.final_situation.orbiting:
        score = START_POINTS - ((500000 * 1/(TARGET_ORBIT_HEIGHT - monitor.max_ap)) +
                                (500000 * 1/(TARGET_ORBIT_HEIGHT - monitor.max_pe)))
    elif monitor.final_situation is monitor.final_situation.orbiting and is_stable_orbit(monitor):
        score = START_POINTS - 1000000 - (500000 * 1/(monitor.closest_approach - TARGET_CLOSEST_APPROACH))

        #TODO Write the final landing condition. Reverse the order to have landing condition be first and pre orbit last

    # Landing on the Mun
    if monitor.body_name == 'Mun':
        score = START_POINTS - 1500000 - (
                250000 * 1 / (DISTANCE_TOLERANCE - monitor.closest_landing_dist) + 250000 * 1 / (
                monitor.lowest_speed_at_touchdown - TARGET_SPEED))
    # Getting to the Mun
    elif monitor.final_situation is monitor.final_situation.orbiting and is_stable_orbit(monitor):
        score = START_POINTS - 1000000 - calculate_closest_approach_decrement(monitor.closest_approach)
    # Getting to orbit
    elif monitor.final_situation is monitor.final_situation.orbiting:
        score = START_POINTS - (calculate_orbit_decrement(monitor.max_ap) +
                                calculate_orbit_decrement(monitor.max_pe))
    # Pre Orbit
    elif monitor.final_situation is monitor.final_situation.flying or \
            monitor.final_situation is monitor.final_situation.sub_orbital:
        score = START_POINTS - calculate_orbit_decrement(monitor.max_ap)
    else:
        score = START_POINTS

    return score


def eval_genomes(genomes, config):
    """Executes genome actions and sets their resulting fitness"""
    connection = krpc.connect(name='TEST')
    rocket_controller = RocketController(connection.space_center.active_vessel)
    game_controller = GameController(connection, rocket_controller)
    for genome_id, genome in genomes:
        # recurrent nn allows us to go back to previous decisions and iterate
        net = neat.nn.RecurrentNetwork.create(genome, config)
        game_controller.restart()  # load game
        monitor = Monitor()
        monitor.set_final_situation(rocket_controller.vessel.situation)
        time.sleep(10)  # TODO: determine time for game to load
        game_controller.launch()  # prepare to fly
        start = time.time()
        elapsed = 0
        while elapsed < 60: # TODO: add failure condition, set time correctly (currently 60 secs)
            #  fly ship!
            genome.fitness = calc_fitness(monitor)  # where does the score come from?
            elapsed = time.time() - start
