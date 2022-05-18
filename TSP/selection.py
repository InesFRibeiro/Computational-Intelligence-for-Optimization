from random import uniform, choice
from operator import attrgetter


def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """

    if population.optim == "max":
        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += individual.fitness
            if position > spin:
                return individual

    elif population.optim == "min":

        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = -uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position -= individual.fitness
            if position < spin:
                return individual

        # Sum total fitness

        # total_invert_fitness = sum([1/i.fitness for i in population if i.fitness != 0 ])
        # # Get a 'position' on the wheel
        # spin = uniform(0, total_invert_fitness)
        # position = 0
        # # Find individual in the position of the spin
        # for individual in population:
        #     if individual.fitness != 0:
        #         position += 1/individual.fitness
        #         if position > spin:
        #             return individual


    else:
        raise Exception("No optimization specified (min or max).")


def tournament(population, size=10):
    """Tournament selection implementation.

    Args:
        population (Population): The population we want to select from.
        size (int): Size of the tournament.

    Returns:
        Individual: Best individual in the tournament.
    """

    # Select individuals based on tournament size
    tournament = [choice(population.individuals) for i in range(size)]
    # Check if the problem is max or min
    if population.optim == 'max':
        return max(tournament, key=attrgetter("fitness"))
    elif population.optim == 'min':
        return min(tournament, key=attrgetter("fitness"))
    else:
        raise Exception("No optimization specified (min or max).")


def ranking_selection(population):
    if population.optim == "max":
        fitness_list = [individual.fitness for individual in population]
        fitness_list, population = zip(*sorted(zip(fitness_list, population), reverse=True))
        fitness_list, population = list(fitness_list), list(population)
        total_positions = sum([i for i in range(1, len(fitness_list) + 1)])
        #prob_list = [i for i in range(1, len(fitness_list) + 1)] / total_positions
        # Get a 'position' on the wheel
        spin = uniform(0, total_positions)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += population.index(individual) +1
            if position > spin:
                return individual

    elif population.optim == "min":
        inverted_fitness_list = [1/individual.fitness for individual in population]
        inverted_fitness_list, population = zip(*sorted(zip(inverted_fitness_list, population), reverse=True))
        inverted_fitness_list, population = list(inverted_fitness_list), list(population)
        total_positions = sum([i for i in range(1, len(inverted_fitness_list) + 1)])
        #prob_list = [i for i in range(1, len(inverted_fitness_list) + 1)] / total_positions
        # Get a 'position' on the wheel
        spin = uniform(0, total_positions)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            #ranking start at 1, but index starts at 0, therefore, we have to add 1
            position += population.index(individual) +1
            if position > spin:
                return individual
    else:
        raise Exception("No optimization specified (min or max).")

