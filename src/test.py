"""
Genetic Algorithm for KSP
Based off https://github.com/CodeReclaimers/neat-python/blob/master/examples/xor/evolve-feedforward.py
NOTE: we are using a recurrent nn, and the above url will give you a feedforward example
"""
from rocket_data_tracker import RocketData
import krpc
from stats_monitor import Monitor
import fitness
import os
import neat


def run(config_file):
    """Sets up nn with specified config and statistic output"""

    # Load config
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(fitness.eval_genomes, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'ksp-neat/NeatConfig.cfg')
    run(config_path)


def update_monitor(monitor, rocket_data:RocketData):
    orbit_data = rocket_data.get_orbit_data()
    dist_from_target =  rocket_data.get_distance()
    closest_approach = rocket_data.get_closest_approach()
    speed = rocket_data.get_speed()
    situation = rocket_data.get_situation()

    # Set the values
    monitor.set_closest_landing_dist(dist_from_target)
    monitor.set_closest_approach(closest_approach)
    monitor.set_lowest_speed_at_touchdown(speed)
    monitor.set_final_situation(situation)
    monitor.set_max_ap(orbit_data[1])
    monitor.set_max_pe(orbit_data[2])
    monitor.set_body_name(orbit_data[0])

# connection = krpc.connect(name='distance_test')
#
# dataObject = RocketData(connection)
# monitor = Monitor()
# while True:
#     update_monitor(monitor, dataObject)
#     score = fitness.calc_fitness(monitor)
#     print(score)
#
#
# connection.close()
# print(monitor)
