from random import randint, sample, randrange


def swap_mutation(individual):
    """Swap mutation for a GA individual

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    # Get two mutation points
    mut_points = sample(range(len(individual)), 2)
    # Swap them
    individual[mut_points[0]], individual[mut_points[1]] = individual[mut_points[1]], individual[mut_points[0]]

    return individual


def inversion_mutation(individual):
    """Inversion mutation for a GA individual

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    # Position of the start and end of substring
    mut_points = sample(range(len(individual)), 2)
    # This method assumes that the second point is after (on the right of) the first one
    # Sort the list
    mut_points.sort()
    # Invert for the mutation
    individual[mut_points[0]:mut_points[1]] = individual[mut_points[0]:mut_points[1]][::-1]

    return individual


def greedy_mutations(individual):

    mut_list = []
    mut_list.extend(individual)
    rng = randrange(0, len(individual))
    city = individual[rng]

    fkcja_celu = individual.get_fitness()
    for i in range(len(individual)):

        if i == 0:
            individual.pop(rng)
        else:
            individual.pop(i - 1)

        individual.insert(i, city)
        tmpfkcja_celu = individual.get_fitness()
        if tmpfkcja_celu < fkcja_celu:
            return individual
    return mut_list

if __name__ == '__main__':
    test = [6, 1, 3, 5, 2, 4, 7]
    test = inversion_mutation(test)

