#from TSP.crossover import order1_crossover
from charles import Population, Individual
from search import hill_climb, sim_annealing
from tsp_data import distance_matrix
from copy import deepcopy
from selection import fps, tournament, ranking_selection
from mutation import swap_mutation, inversion_mutation, greedy_mutations
from crossover import cycle_co, pmx_co, order1_crossover, cx_crossover
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

selection_list = [fps, tournament, ranking_selection]
final_pop_list = []

for selec in selection_list:
    num_gens = 100
    n = 30
    final_pops = []

    evo_list_base = []
    for i in range(n):

        pop = Population(
            size=20,
            sol_size=len(distance_matrix[0]),
            valid_set=[i for i in range(len(distance_matrix[0]))],
            replacement=False,
            optim="min",
        )

        evolved_pop = pop.evolve(
            gens=num_gens,
            select=selec,
            crossover=order1_crossover,
            mutate=greedy_mutations,
            co_p=0.9,
            mu_p=0.1,
            elitism=True
        )

        evo_list_base.append(evolved_pop[0])
        final_pops.append(evolved_pop[1].getIndivs())

    #print(final_pops[0])
    print(final_pops[0][-1].returnPath())
    final_pop_list.append(final_pops)

    avg_dict_base = evo_list_base[0]

    for edict in range(1,len(evo_list_base)):

        for gen in evo_list_base[edict]:
            avg_dict_base[gen] += evo_list_base[edict][gen]

    for avg in avg_dict_base:
        avg_dict_base[avg] /= num_gens

    #print(avg_dict_base)
        # row = 2*j//V
        # col = max(j*abs(2*j//V-1),j-V//2)
        
        # for edict in range(len(evo_list)):  
        #     plt.plot(evo_list[edict].keys(),\
        #         evo_list[edict].values(),label='Run '+str(edict))
        #     plt.legend()

        # plt.show()

    plt.plot(avg_dict_base.keys(),\
        avg_dict_base.values(), \
            label = selec.__name__)

plt.title("Selection method comparisons")
plt.legend()
plt.show()