from random import randint, uniform, sample, random, randrange
from copy import deepcopy


def cycle_co(p1, p2):
    """Implementation of cycle crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """

    # Offspring placeholders - None values make it easy to debug for errors
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p2)
    # While there are still None values in offspring, get the first index of
    # None and start a "cycle" according to the cycle crossover method
    while None in offspring1:
        index = offspring1.index(None)

        val1 = p1[index]
        val2 = p2[index]

        while val1 != val2:
            offspring1[index] = p1[index]
            offspring2[index] = p2[index]
            val2 = p2[index]
            index = p1.index(val2)

        for element in offspring1:
            if element is None:
                index = offspring1.index(None)
                if offspring1[index] is None:
                    offspring1[index] = p2[index]
                    offspring2[index] = p1[index]

    return offspring1, offspring2

def new_pmx_co(p1,p2):
    """Implementation of partially matched/mapped crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """

    co_points = sample(range(len(p1)), 2)
    co_points.sort()
    #co_points = (0,2)


    def new_PMX(x,y):
        o = [None] * len(x)

        o[co_points[0]:co_points[1]] = x[co_points[0]:co_points[1]]

        z = set(y[co_points[0]:co_points[1]]) - set(x[co_points[0]:co_points[1]])

        for i in z:
            temp = i
            index = y.index(x[y.index(temp)])
            while o[index] != None:
                temp = index
                index = y.index(x[temp])
            o[index] = i

        while None in o:
            index = o.index(None)
            o[index] = y[index]
        return o

    o1, o2 = new_PMX(p1,p2), new_PMX(p2,p1)
    return o1, o2

def corrected_co(parent1, parent2):
    """Implementation of regular crossover with correction
    for duplicates.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    def process_gen_repeated(copy_child1, copy_child2, pos):
        count1 = 0
        for gen1 in copy_child1[:pos]:
            repeat = 0
            repeat = copy_child1.count(gen1)
            if repeat > 1:  # If need to fix repeated gen
                count2 = 0
                for gen2 in parent1[pos:]:  # Choose next available gen
                    if gen2 not in copy_child1:
                        child1[count1] = parent1[pos:][count2]
                    count2 += 1
            count1 += 1

        count1 = 0
        for gen1 in copy_child2[:pos]:
            repeat = 0
            repeat = copy_child2.count(gen1)
            if repeat > 1:  # If need to fix repeated gen
                count2 = 0
                for gen2 in parent2[pos:]:  # Choose next available gen
                    if gen2 not in copy_child2:
                        child2[count1] = parent2[pos:][count2]
                    count2 += 1
            count1 += 1

        return child1, child2

    pos = randrange(1, len(parent1) - 1)
    child1 = parent1[:pos] + parent2[pos:]
    child2 = parent2[:pos] + parent1[pos:]

    return process_gen_repeated(child1, child2, pos)

def cxOrdered(parent1, parent2):
    """Executes an ordered crossover (OX) on the input
    individuals. The two individuals are modified in place. This crossover
    expects :term:`sequence` individuals of indices, the result for any other
    type of individuals is unpredictable.
    :param parent1: The first individual participating in the crossover.
    :param parent2: The second individual participating in the crossover.
    :returns: A tuple of two individuals.
    Moreover, this crossover generates holes in the input
    individuals. A hole is created when an attribute of an individual is
    between the two crossover points of the other individual. Then it rotates
    the element so that all holes are between the crossover points and fills
    them with the removed elements in order. For more details see
    [Goldberg1989]_.
    This function uses the :func:`~random.sample` function from the python base
    :mod:`random` module.
    .. [Goldberg1989] Goldberg. Genetic algorithms in search,
       optimization and machine learning. Addison Wesley, 1989
    """
    size = min(len(parent1), len(parent2))
    a, b = sample(range(size), 2)
    if a > b:
        a, b = b, a

    holes1, holes2 = [True] * size, [True] * size
    for i in range(size):
        if i < a or i > b:
            holes1[parent2[i]] = False
            holes2[parent1[i]] = False

    # We must keep the original values somewhere before scrambling everything
    temp1, temp2 = parent1, parent2
    k1, k2 = b + 1, b + 1
    for i in range(size):
        if not holes1[temp1[(i + b + 1) % size]]:
            parent1[k1 % size] = temp1[(i + b + 1) % size]
            k1 += 1

        if not holes2[temp2[(i + b + 1) % size]]:
            parent2[k2 % size] = temp2[(i + b + 1) % size]
            k2 += 1

    # Swap the content between a and b (included)
    for i in range(a, b + 1):
        parent1[i], parent2[i] = parent2[i], parent1[i]

    return parent1, parent2


if __name__ == '__main__':
    p1, p2 = [9, 8, 4, 5, 6, 7, 1, 3, 2, 10], [8, 7, 1, 2, 3, 10, 9, 5, 4, 6]
    #p1, p2 = [1, 2, 3, 4, 5, 6, 7, 8, 9], [9, 3, 7, 8, 2, 6, 5, 1, 4]
    #p1, p2 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], [0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3]
    o1, o2 = new_pmx_co(p1, p2)

