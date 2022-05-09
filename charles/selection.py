from random import uniform, choice, randint
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
        raise NotImplementedError

    else:
        raise Exception("No optimization specified (min or max).")

def tournament(population, size=5):
    """Tournament selection implementation.

    Args:
        population (Population): The population we want to select from.
        size (int): Size of the tournament.

    Returns:
        Individual: Best individual in the tournament.
    """

    # Select individuals based on tournament size
    tournament = [choice(population.individuals) for i in range(size)]

    results = sorted(tournament, key=attrgetter("fitness"))

    # min(tournament, key=attrgetter("fitness"))

    selection_rate = 0.80
    r = uniform(0, 1.1)
    while (r > 1):  # Outside [0, 1] boundary. Choose another.
        r = uniform(0, 1.1)
    if (r < selection_rate):
        return results[0]
    else:
        return results[1]

    # else:
    #     if population.optim == 'max':
            
    # elif population.optim == 'min':
    #     return max(tournament, key=attrgetter("fitness"))
        
    # else:
    #     raise Exception("No optimization specified (min or max).")

