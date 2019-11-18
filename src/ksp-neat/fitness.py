import time

import krpc
import neat

from stats_monitor import Monitor

def is_stable_orbit(monitor):
    STABLE_HEIGHT = 70000
    return monitor.max_ap > STABLE_HEIGHT and monitor.max_pe > STABLE_HEIGHT

def calc_fitness(monitor):
    """
    The goal for the rockets is to get to a fitness value of zero.
    We start from 2,000,000 as a fitness score
    Fitness is calculated in four stages'

    1. Pre orbit of Kerbin. We want to reward getting to orbit first before flying towards the Mun
    Therefore we deduct points for advancing towards orbit.

    2. If the situation recorded is orbit then we calculate if it is a valid orbit. 100km orbit will be ideal so
    The closer to that target the rocket gets. the more points that will be deducted. These first two steps can bring
    the score down to a minimum of 1,000,000 points.

    3. Hohmann transfer to the Mun: The AI will get more points dedeucted for getting a waypoint that encouters the Mun.
    This can bring the score down to 500,000 points.

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


def eval_genomes(genomes, config, game_controller):
    """Executes genome actions and sets their resulting fitness"""
    for genome_id, genome in genomes:
        # recurrent nn allows us to go back to previous decisions and iterate
        net = neat.nn.RecurrentNetwork.create(genome, config)
        game_controller.restart()  # load game
        monitor = Monitor()
        time.sleep(3)  # TODO: determine time for game to load
        game_controller.launch()  # prepare to fly
        # while game_controller.not_failed(): TODO
        #  fly ship!
        genome.fitness = calc_fitness(monitor)  # where does the score come from?
