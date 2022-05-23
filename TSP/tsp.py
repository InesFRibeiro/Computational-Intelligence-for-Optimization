#from TSP.crossover import order1_crossover
from charles import Population, Individual
from search import hill_climb, sim_annealing
from tsp_data import distance_matrix
from copy import deepcopy
from selection import fps, tournament, ranking_selection
from mutation import swap_mutation, inversion_mutation, scramble
from crossover import cycle_co, new_pmx_co, \
    corrected_co, cxOrdered
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

# List of evolved populations
final_pop_list = []

############ Comparing selection, crossover, and mutation methods

# Available selection methods
selection_list = [fps, tournament, ranking_selection]
# Available crossover methods
crossover_list = [cycle_co, new_pmx_co, corrected_co]#, cxOrdered]
# pôr depois o cxordered outra vez, mas tava lento

fig, axes = plt.subplots(1, len(crossover_list), figsize = [20, 8])

for ax, crosser in zip(axes.flatten(), crossover_list):
    for selec in selection_list:
        # All 3 available selection methods are tested
        #for each crossover method

        num_gens = 100
        n = 30
        final_pops = []

        evo_list_base = []
        for i in range(n): 
            # 30 different tests are ran with each set of
            #parameters in order to achieve statistical significance

            pop = Population(
                size=20,
                sol_size=len(distance_matrix[0]),
                valid_set=[i for i in range(len(distance_matrix[0]))],
                replacement=False,
                optim="min",
            )
            # Creating a Population of 20 possible solutions

            evolved_pop = pop.evolve(
                gens=num_gens,
                select=selec,
                crossover=crosser,
                mutate=scramble,
                co_p=0.9,
                mu_p=0.1,
                elitism=True
            )
            # The created population undergoes 100 generations
            #of evolution, with the current selection and 
            #crossover methods

            evo_list_base.append(evolved_pop[0])
            # The list of best fitnesses per generation is stored
            final_pops.append(evolved_pop[1].getIndivs())
            # The last generation is stored

        print(final_pops[0][-1].returnPath())
        # Returns a solution for testing purposes
        #(make it be the best one - banana)
        final_pop_list.append(final_pops)

        avg_dict_base = evo_list_base[0]
        # Initializes the dictionary of average best fitness per gen

        for edict in range(1,len(evo_list_base)):

            for gen in evo_list_base[edict]:
                avg_dict_base[gen] += evo_list_base[edict][gen]
                # Adds registered best fitnesses for every gen
                #on each new try

        for avg in avg_dict_base:
            avg_dict_base[avg] /= num_gens
            # Computes averages

        ax.plot(avg_dict_base.keys(),\
            avg_dict_base.values(), \
                label = selec.__name__)
            # Plots averages

    ax.set_title(crosser.__name__ + " crossover")
    ax.legend()

plt.suptitle("Selection and crossover comparisons")
#plt.legend()
plt.show()