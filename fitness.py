import neat
import game
import time


def calc_fitness(vessel, flight):
    """
    Determines the score for how well a vessel performs (higher is better)

    :param vessel: the current ship
    :param flight: contains variables for the ship's fly (like altitude)
    :return: float representing how well a vessel performed
    """
    score = 0
    # TODO: calculate how close to the moon we are
    return score  # should be a float


def eval_genomes(genomes, config):
    """Executes genome actions and sets their resulting fitness"""
    game_instance = game.Game()
    for genome_id, genome in genomes:
        # recurrent nn allows us to go back to previous decisions and iterate
        net = neat.nn.RecurrentNetwork.create(genome, config)
        game_instance.restart()
        time.sleep(3)  # TODO: determine time for game to load
        game_instance.launch()  # fly ship!
        genome.fitness = calc_fitness(game_instance.vessel, game_instance.flight)
