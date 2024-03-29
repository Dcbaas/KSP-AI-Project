"""
Genetic Algorithm for KSP
Based off https://github.com/CodeReclaimers/neat-python/blob/master/examples/xor/evolve-feedforward.py
NOTE: we are using a recurrent nn, and the above url will give you a feedforward example
"""
from ksp_neat.fitness import eval_genomes
import os
import sys
import neat


def run(config_file, isCheckpoint:bool):
    """
    Sets up nn with specified config and statistic output

    If a save file was specified when starting the program the program will load neural network data from the save.
    Otherwise, it will use NeatConfig.cfg to load the configuration
    :param config_file: The config file being loaded from
    :param isCheckpoint: Flag for indicating that we are loading from a checkpoint
    :return: None
    """

    if isCheckpoint:
        p = neat.Checkpointer.restore_checkpoint(config_file)
    else:
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
    winner = p.run(eval_genomes,  1500)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    if len(sys.argv) == 2:
        config_path = os.path.join(local_dir, sys.argv[1])
        run(config_path, True)
    else:
        config_path = os.path.join(local_dir, 'ksp_neat/NeatConfig.cfg')
        run(config_path, False)

