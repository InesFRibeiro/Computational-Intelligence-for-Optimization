from charles.charles import Population, Individual, Nd
from charles.search import hill_climb, sim_annealing
from copy import deepcopy
from charles.selection import fps, tournament
from charles.mutation import swap_mutation, sudoku_mutation
from charles.crossover import single_point_co
from random import random

from operator import attrgetter
import numpy as np

 # Number of digits (in the case of standard Sudoku puzzles, this is 9x9).

def update_fitness(self): #not berfin
    """ The fitness of a individual solution is determined by how close it is to being the actual solution to the puzzle.
    The actual solution (i.e. the 'fittest') is defined as a 9x9 grid of numbers in the range [1, 9]
    where each row, column and 3x3 block contains the numbers [1, 9] without any duplicates (see e.g. http://www.sudoku.com/);
    if there are any duplicates then the fitness will be lower. """

    column_count = np.zeros(Nd)
    block_count = np.zeros(Nd)
    column_sum = 0
    block_sum = 0

    self.values = self.values.astype(int)
    # For each column....
    for j in range(0, Nd):
        for i in range(0, Nd):
            column_count[self.values[i][j] - 1] += 1

        # unique
        # column_sum += (1.0 / len(set(column_count))) / Nd
        # set
        # for k in range(len(column_count)):
        #     if column_count[k] != 0:
        #         column_sum += (1/Nd)/Nd
        # duplicate
        for k in range(len(column_count)):
            if column_count[k] == 1:
                column_sum += (1/Nd)/Nd
        column_count = np.zeros(Nd)

    # For each block...
    for i in range(0, Nd, 3):
        for j in range(0, Nd, 3):
            block_count[self.values[i][j] - 1] += 1
            block_count[self.values[i][j + 1] - 1] += 1
            block_count[self.values[i][j + 2] - 1] += 1

            block_count[self.values[i + 1][j] - 1] += 1
            block_count[self.values[i + 1][j + 1] - 1] += 1
            block_count[self.values[i + 1][j + 2] - 1] += 1

            block_count[self.values[i + 2][j] - 1] += 1
            block_count[self.values[i + 2][j + 1] - 1] += 1
            block_count[self.values[i + 2][j + 2] - 1] += 1

            # unique
            # block_sum += (1.0 / len(set(block_count))) / Nd
            # set
            # for k in range(len(block_count)):
            #     if block_count[k] != 0:
            #         block_sum += (1/Nd)/Nd
            # duplicate
            for k in range(len(block_count)):
                if block_count[k] == 1:
                    block_sum += (1/Nd)/Nd
            block_count = np.zeros(Nd)

    # Calculate overall fitness.
    if int(column_sum) == 1 and int(block_sum) == 1:
        fitness = 1.0
    else:
        fitness = column_sum * block_sum

    self.fitness = fitness

Individual.update_fitness = update_fitness




        


class Fixed(Individual):
    """ fixed/given values. """

    def __init__(self, values):
        self.values = values
        return

    def is_row_duplicate(self, row, value):
        """ Check duplicate in a row. """
        for column in range(0, Nd):
            if self.values[row][column] == value:
                return True
        return False

    def is_column_duplicate(self, column, value):
        """ Check duplicate in a column. """
        for row in range(0, Nd):
            if self.values[row][column] == value:
                return True
        return False

    def is_block_duplicate(self, row, column, value):
        """ Check duplicate in a 3 x 3 block. """
        i = 3 * (int(row / 3))
        j = 3 * (int(column / 3))

        if ((self.values[i][j] == value)
            or (self.values[i][j + 1] == value)
            or (self.values[i][j + 2] == value)
            or (self.values[i + 1][j] == value)
            or (self.values[i + 1][j + 1] == value)
            or (self.values[i + 1][j + 2] == value)
            or (self.values[i + 2][j] == value)
            or (self.values[i + 2][j + 1] == value)
            or (self.values[i + 2][j + 2] == value)):
            return True
        else:
            return False

    def make_index(self, v):
        if v <= 2:
            return 0
        elif v <= 5:
            return 3
        else:
            return 6

    def no_duplicates(self):
        for row in range(0, Nd):
            for col in range(0, Nd):
                if self.values[row][col] != 0:

                    cnt1 = list(self.values[row]).count(self.values[row][col])
                    cnt2 = list(self.values[:,col]).count(self.values[row][col])

                    block_values = [y[self.make_index(col):self.make_index(col)+3] for y in
                                    self.values[self.make_index(row):self.make_index(row)+3]]
                    block_values_ = [int(x) for y in block_values for x in y]
                    cnt3 = block_values_.count(self.values[row][col])

                    if cnt1 > 1 or cnt2 > 1 or cnt3 > 1:
                        return False
        return True



class Tournament(object):
    """ The crossover function requires two parents to be selected from the population pool. The Tournament class is used to do this.

    Two individuals are selected from the population pool and a random number in [0, 1] is chosen. If this number is less than the 'selection rate' (e.g. 0.85), then the fitter individual is selected; otherwise, the weaker one is selected.
    """

    def __init__(self):
        return

    def compete(self, individuals):
        """ Pick 2 random individuals from the population and get them to compete against each other. """
        c1 = individuals[random.randint(0, len(individuals) - 1)]
        c2 = individuals[random.randint(0, len(individuals) - 1)]
        f1 = c1.fitness
        f2 = c2.fitness

        # Find the fittest and the weakest.
        if (f1 > f2):
            fittest = c1
            weakest = c2
        else:
            fittest = c2
            weakest = c1

        # selection_rate = 0.85
        selection_rate = 0.80
        r = random.uniform(0, 1.1)
        while (r > 1):  # Outside [0, 1] boundary. Choose another.
            r = random.uniform(0, 1.1)
        if (r < selection_rate):
            return fittest
        else:
            return weakest


class CycleCrossover(object):
    """ Crossover relates to the analogy of genes within each parent individual
    mixing together in the hopes of creating a fitter child individual.
    Cycle crossover is used here (see e.g. A. E. Eiben, J. E. Smith.
    Introduction to Evolutionary Computing. Springer, 2007). """

    def __init__(self):
        return

    def crossover(self, parent1, parent2, crossover_rate):
        """ Create two new child individuals by crossing over parent genes. """
        child1 = Individual()
        child2 = Individual()

        # Make a copy of the parent genes.
        child1.values = np.copy(parent1.values)
        child2.values = np.copy(parent2.values)

        r = random.uniform(0, 1.1)
        while (r > 1):  # Outside [0, 1] boundary. Choose another.
            r = random.uniform(0, 1.1)

        # Perform crossover.
        if (r < crossover_rate):
            # Pick a crossover point. Crossover must have at least 1 row (and at most Nd-1) rows.
            crossover_point1 = random.randint(0, 8)
            crossover_point2 = random.randint(1, 9)
            while (crossover_point1 == crossover_point2):
                crossover_point1 = random.randint(0, 8)
                crossover_point2 = random.randint(1, 9)

            if (crossover_point1 > crossover_point2):
                temp = crossover_point1
                crossover_point1 = crossover_point2
                crossover_point2 = temp

            for i in range(crossover_point1, crossover_point2):
                child1.values[i], child2.values[i] = self.crossover_rows(child1.values[i], child2.values[i])

        return child1, child2

    def crossover_rows(self, row1, row2):
        child_row1 = np.zeros(Nd)
        child_row2 = np.zeros(Nd)

        remaining = range(1, Nd + 1)
        cycle = 0

        while ((0 in child_row1) and (0 in child_row2)):  # While child rows not complete...
            if (cycle % 2 == 0):  # Even cycles.
                # Assign next unused value.
                index = self.find_unused(row1, remaining)
                start = row1[index]
                remaining.remove(row1[index])
                child_row1[index] = row1[index]
                child_row2[index] = row2[index]
                next = row2[index]

                while (next != start):  # While cycle not done...
                    index = self.find_value(row1, next)
                    child_row1[index] = row1[index]
                    remaining.remove(row1[index])
                    child_row2[index] = row2[index]
                    next = row2[index]

                cycle += 1

            else:  # Odd cycle - flip values.
                index = self.find_unused(row1, remaining)
                start = row1[index]
                remaining.remove(row1[index])
                child_row1[index] = row2[index]
                child_row2[index] = row1[index]
                next = row2[index]

                while (next != start):  # While cycle not done...
                    index = self.find_value(row1, next)
                    child_row1[index] = row2[index]
                    remaining.remove(row1[index])
                    child_row2[index] = row1[index]
                    next = row2[index]

                cycle += 1

        return child_row1, child_row2

    def find_unused(self, parent_row, remaining):
        for i in range(0, len(parent_row)):
            if (parent_row[i] in remaining):
                return i

    def find_value(self, parent_row, value):
        for i in range(0, len(parent_row)):
            if (parent_row[i] == value):
                return i

class Sudoku(object):
    """ Solves a given Sudoku puzzle using a genetic algorithm. """

    def __init__(self):
        self.given = None
        return

    def load(self, p):
        #values = np.array(list(p.replace(".","0"))).reshape((Nd, Nd)).astype(int)
        self.given = Fixed(p)
        return

    def solve(self):

        Nc = 1000  # Number of individuals (i.e. population size).
        Ne = int(0.05 * Nc)  # Number of elites.
        Ng = 10000  # Number of generations.
        Nm = 0  # Number of mutations.

        # Mutation parameters.
        phi = 0
        sigma = 1
        mutation_rate = 0.06

        # Check given one first
        if self.given.no_duplicates() == False:
            return (-1, 1)

        # Create an initial population.
        self.population = Population()
        print("create an initial population.")
        if self.population.seed(Nc, self.given) ==  1:
            pass
        else:
            return (-1, 1)

        # For up to 10000 generations...
        stale = 0
        for generation in range(0, Ng):

            # Check for a solution.
            best_fitness = 0.0
            #best_fitness_population_values = self.population.individuals[0].values
            for c in range(0, Nc):
                fitness = self.population.individuals[c].fitness
                if (fitness == 1):
                    print("Solution found at generation %d!" % generation)
                    return (generation, self.population.individuals[c])

                # Find the best fitness and corresponding chromosome
                if (fitness > best_fitness):
                    best_fitness = fitness
                    #best_fitness_population_values = self.population.individuals[c].values

            print("Generation:", generation, " Best fitness:", best_fitness)
            #print(best_fitness_population_values)

            # Create the next population.
            next_population = []

            # Select elites (the fittest individuals) and preserve them for the next generation.
            self.population.sort()
            elites = []
            for e in range(0, Ne):
                elite = Individual()
                elite.values = np.copy(self.population.individuals[e].values)
                elites.append(elite)

            # Create the rest of the individuals.
            for count in range(Ne, Nc, 2):
                # Select parents from population via a tournament.
 
                parent1 = tournament(self.population.individuals)
                parent2 = tournament(self.population.individuals)

                ## Cross-over.
                cc = CycleCrossover()
                child1, child2 = cc.crossover(parent1, parent2, crossover_rate=1.0)

                # Mutate child1.
                child1.update_fitness()
                old_fitness = child1.fitness
                success = child1.mutate(mutation_rate, self.given)
                child1.update_fitness()
                if (success):
                    Nm += 1
                    if (child1.fitness > old_fitness):  # Used to calculate the relative success rate of mutations.
                        phi = phi + 1

                # Mutate child2.
                child2.update_fitness()
                old_fitness = child2.fitness
                success = child2.mutate(mutation_rate, self.given)
                child2.update_fitness()
                if (success):
                    Nm += 1
                    if (child2.fitness > old_fitness):  # Used to calculate the relative success rate of mutations.
                        phi = phi + 1

                # Add children to new population.
                next_population.append(child1)
                next_population.append(child2)

            # Append elites onto the end of the population. These will not have been affected by crossover or mutation.
            for e in range(0, Ne):
                next_population.append(elites[e])

            # Select next generation.
            self.population.individuals = next_population
            self.population.update_fitness()

            # Calculate new adaptive mutation rate (based on Rechenberg's 1/5 success rule).
            # This is to stop too much mutation as the fitness progresses towards unity.
            if (Nm == 0):
                phi = 0  # Avoid divide by zero.
            else:
                phi = phi / Nm

            if (phi > 0.2):
                sigma = sigma / 0.998
            elif (phi < 0.2):
                sigma = sigma * 0.998

            mutation_rate = abs(np.random.normal(loc=0.0, scale=sigma, size=None))

            # Check for stale population.
            self.population.sort()
            if (self.population.individuals[0].fitness != self.population.individuals[1].fitness):
                stale = 0
            else:
                stale += 1

            # Re-seed the population if 100 generations have passed
            # with the fittest two individuals always having the same fitness.
            if (stale >= 100):
                print("The population has gone stale. Re-seeding...")
                self.population.seed(Nc, self.given)
                stale = 0
                sigma = 1
                phi = 0
                mutation_rate = 0.06

        print("No solution found.")
        return (-2, 1)