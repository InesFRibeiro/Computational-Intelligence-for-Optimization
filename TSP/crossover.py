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


def pmx_co(p1, p2): # doesn't work
    """Implementation of partially matched/mapped crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    co_points = sample(range(len(p1)), 2)
    co_points.sort()

    # dictionary creation using the segment elements from both parents
    # the dictionary will be working two ways
    keys = p1[co_points[0]:co_points[1]] + p2[co_points[0]:co_points[1]]
    values = p2[co_points[0]:co_points[1]] + p1[co_points[0]:co_points[1]]
    # segment dictionary
    segment = {keys[i]: values[i] for i in range(len(keys))}

    # empty offsprings
    o1 = [None] * len(p1)
    o2 = [None] * len(p2)

    # where pmx happens
    def pmx(o, p):
        for i, element in enumerate(p):
            # if element not in the segment, copy
            if element not in segment:
                o[i] = p[i]
            # if element in the segment, take the value of the key from
            # segment/dictionary
            else:
                o[i] = segment.get(element)
        return o

    # repeat the procedure for each offspring
    o1 = pmx(o1, p1)
    o2 = pmx(o2, p2)
    return o1, o2

def new_pmx_co(p1,p2):
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




def get_two_diff_order_index(start=0, stop=1, order=True, diff=True):
    """
    Returns two integers from a range, they can be:
        put in order (default) or unordered
        always different(default) or can be repeated
    start - integer (default = 0)
    stop - integer (default= 1)
    order - boolean ( default= True)
    """
    my_range = stop - start
    first = int(my_range * random())+start
    second = int(my_range * random())+start

    #first = randint(start, stop)
    #second = randint(start, stop)

    if diff:
        while first == second:
            second = int( my_range * random()) + start
            #second = randint(start, stop)
    if order:
        if first > second:
            second, first = first, second

    return first, second


def order1_crossover(solution1, solution2): # bad representation
    # copy the parents to the children because we only need to change the middle part and the repeated elements
    offspring1 = deepcopy(solution1)
    offspring2 = deepcopy(solution2)

    # get two different, ordered, indexes
    crosspoint1, crosspoint2 = get_two_diff_order_index(0, (len(solution1.representation) - 1))

    # indexes of the elements not in the middle
    sub = [*range((crosspoint2+1), len(offspring1.representation))]+[*range(0, crosspoint1)]
    len_sub = len(sub)
    j = 0
    k = 0

    if crosspoint2 == (len(solution1.representation)-1) and crosspoint1 == 0:
        return solution1, solution2
    else:
                        # order by which elements must be considered
        for i in [*range((crosspoint2+1), len(offspring1.representation))]+[*range(0, (crosspoint2+1))]:

            # replace offspring1 if element is not in the middle
            if solution2.representation[i] not in solution1.representation[crosspoint1:(crosspoint2+1)]:
                offspring1.representation[sub[j]] = solution2.representation[i]
                j += 1

            # replace offspring2 if element is not in the middle
            if solution1.representation[i] not in solution2.representation[crosspoint1:(crosspoint2+1)]:
                offspring2.representation[sub[k]] = solution1.representation[i]
                k += 1

            if j == len_sub and k == len_sub:
                break

        return offspring1, offspring2

def cx_crossover(parent1, parent2):

    def process_gen_repeated(copy_child1, copy_child2):
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

        return [child1, child2]

    pos = randrange(1, len(parent1) - 1)
    child1 = parent1[:pos] + parent2[pos:]
    child2 = parent2[:pos] + parent1[pos:]

    return process_gen_repeated(child1, child2)

if __name__ == '__main__':
    p1, p2 = [9, 8, 4, 5, 6, 7, 1, 3, 2, 10], [8, 7, 1, 2, 3, 10, 9, 5, 4, 6]
    #p1, p2 = [1, 2, 3, 4, 5, 6, 7, 8, 9], [9, 3, 7, 8, 2, 6, 5, 1, 4]
    #p1, p2 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], [0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3]
    o1, o2 = pmx_co(p1, p2)

