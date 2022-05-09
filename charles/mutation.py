from random import randint, sample, uniform

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

def sudoku_mutation(individual, mutation_rate, given):

    r = uniform(0, 1.1)
    while r > 1:  # Outside [0, 1] boundary - choose another
        r = uniform(0, 1.1)

    success = False
    if r < mutation_rate:  # Mutate.
        while not success:
            row1 = randint(0, 8)
            row2 = randint(0, 8)
            row2 = row1

            from_column = randint(0, 8)
            to_column = randint(0, 8)
            while from_column == to_column:
                from_column = randint(0, 8)
                to_column = randint(0, 8)

             # Check if the two places are free to swap
            if given.values[row1][from_column] == 0 and given.values[row1][to_column] == 0:
                # ...and that we are not causing a duplicate in the rows' columns.
                if not given.is_column_duplicate(to_column, individual.values[row1][from_column]) and not given.is_column_duplicate(from_column, individual.values[row2][to_column]) and not given.is_block_duplicate(row2, to_column, individual.values[row1][from_column]) and not given.is_block_duplicate(row1, from_column, individual.values[row2][to_column]):
                    # Swap values.
                    temp = individual.values[row2][to_column]
                    individual.values[row2][to_column] = individual.values[row1][from_column]
                    individual.values[row1][from_column] = temp
                    success = True

    return success

if __name__ == '__main__':
    test = [0, 0, 0, 0, 1, 1, 1, 1]
    test = swap_mutation(test)
