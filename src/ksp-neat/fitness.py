import krpc
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


def calc_fitness(monitor:Monitor):
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
