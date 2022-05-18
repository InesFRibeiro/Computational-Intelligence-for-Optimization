from charles import Population, Individual
from search import hill_climb, sim_annealing
from tsp_data import distance_matrix
from copy import deepcopy
from selection import fps, tournament, ranking_selection
from mutation import swap_mutation, inversion_mutation
from crossover import cycle_co, pmx_co
import matplotlib.pyplot as plt

def get_fitness(self):
    """A simple objective function to calculate distances
    for the TSP problem.

    Returns:
        int: the total distance of the path
    """
    fitness = 0
    for i in range(len(self.representation)):
        fitness += distance_matrix[self.representation[i - 1]][self.representation[i]]
    return int(fitness)

def get_fitness_2():
    pass

def get_neighbours(self):
    """A neighbourhood function for the TSP problem. Switches
    indexes around in pairs.

    Returns:
        list: a list of individuals
    """
    n = [deepcopy(self.representation) for i in range(len(self.representation) - 1)]

    for count, i in enumerate(n):
        i[count], i[count + 1] = i[count + 1], i[count]

    n = [Individual(i) for i in n]
    return n


# Monkey patching
Individual.get_fitness = get_fitness
Individual.get_neighbours = get_neighbours


n = 5
V = 6

for j in range(V):

    evo_list = []
    for i in range(n):

        pop = Population(
            size=20,
            sol_size=len(distance_matrix[0]),
            valid_set=[i for i in range(len(distance_matrix[0]))],
            replacement=False,
            optim="min",
        )

        evo_list.append(pop.evolve(
            gens=100,
            select=tournament,
            crossover=pmx_co,
            mutate=inversion_mutation,
            co_p=0.9,
            mu_p=0.1,
            elitism=True
        ))

    print(evo_list)

    row = 2*j//V
    col = max(j*abs(2*j//V-1),j-V//2)
    
    for edict in range(len(evo_list)):  
        plt.plot(evo_list[edict].keys(),\
            evo_list[edict].values(),label='Run '+str(edict))
        plt.legend()

    plt.show()
    