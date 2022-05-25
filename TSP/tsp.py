#from TSP.crossover import order1_crossover
from charles import Population, Individual
from search import hill_climb, sim_annealing
from tsp_data2 import cities, distance_matrix
from copy import deepcopy
from selection import fps, tournament, ranking_selection
from mutation import swap_mutation, inversion_mutation, \
    scramble, insert
from crossover import cycle_co, new_pmx_co, \
    corrected_co, cxOrdered
import matplotlib.pyplot as plt
import numpy as np

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
crossover_list = [cycle_co, new_pmx_co, corrected_co, cxOrdered]
# pôr depois o cxordered outra vez, mas tava lento
# Available mutation methods
mutation_list = [swap_mutation, inversion_mutation, scramble, insert]

optim="min"

avg_fit_dict = {}
best_fit_dict = {}

for mute in mutation_list:
    fig, axes = plt.subplots(1, len(crossover_list), figsize = [20, 8])
    for ax, crosser in zip(axes.flatten(), crossover_list):
        for selec in selection_list:
            # All 3 available selection methods are tested
            #for each crossover method

            num_gens = 100
            n = 30
            final_pops = []

            evo_list_base = []
            
            if optim == "min":
                best_fit = np.inf
            else:
                best_fit = -np.inf

            for i in range(n): 
                # 30 different tests are ran with each set of
                #parameters in order to achieve statistical significance

                pop = Population(
                    size=20,
                    sol_size=len(distance_matrix[0]),
                    valid_set=[i for i in range(len(distance_matrix[0]))],
                    replacement=False,
                    optim=optim,
                )
                # Creating a Population of 20 possible solutions

                evolved_pop = pop.evolve(
                    gens=num_gens,
                    select=selec,
                    crossover=crosser,
                    mutate=mute,
                    co_p=0.9,
                    mu_p=0.1,
                    elitism=True
                )
                # The created population undergoes 100 generations
                #of evolution, with the current selection and 
                #crossover methods

                evo_list_base.append(evolved_pop)#[0])
                # The list of best fitnesses per generation is stored
                final_pops.append(pop)#[1])
                # The last generation is stored

                if pop.getOptim() == "min":
                    if best_fit > pop.getBestFit().get_fitness():
                        best_one = pop.getBestFit()
                        best_fit = best_one.get_fitness()
                else:
                    if best_fit < pop.getBestFit().get_fitness():
                        best_one = pop.getBestFit()
                        best_fit = best_one.get_fitness()

            best_fit_dict["Selection method: " + \
                selec.__name__ + "; Crossover method: " + \
                crosser.__name__ + "; Mutation method: " + \
                mute.__name__ + " "] = best_one
            # Stores best fitness individual of last generation 
            #for each algorithm

            final_pop_list.append(final_pops)

            avg_dict_base = evo_list_base[0]
            # Initializes the dictionary of average best fitness per gen

            for edict in range(1,len(evo_list_base)):

                for gen in evo_list_base[edict]:
                    avg_dict_base[gen] += evo_list_base[edict][gen]
                    # Adds registered best fitnesses for every gen
                    #on each new try

            for avg in avg_dict_base:
                avg_dict_base[avg] /= n
                # Computes averages

            avg_fit_dict["Selection method: " + \
                selec.__name__ + "; Crossover method: " + \
                crosser.__name__ + "; Mutation method: " + \
                mute.__name__ + " "] = avg_dict_base[99]

            # Stores average fitness of last generation 
            #for each algorithm

            ax.plot(avg_dict_base.keys(),\
                avg_dict_base.values(), \
                    label = selec.__name__)
                # Plots averages

        ax.set_title(crosser.__name__ + " crossover")
        ax.legend()

    plt.suptitle("Selection and crossover comparisons "+\
        "for mutation " + mute.__name__)
    #plt.legend()
    plt.show()
    #plt.clf()

best_avg_fit = max(avg_fit_dict)
best_best_fit = max(best_fit_dict)

print("The best average fitness obtained is: " + \
    str(avg_fit_dict[best_avg_fit]) + \
        ";\nObtained for the model with the parameters: " + \
            best_avg_fit)

full_path = [cities[c] for c in \
    best_fit_dict[best_best_fit].returnPath()]

full_path_str = ""
for t in full_path:
    full_path_str = full_path_str + t + " -> "

full_path_str = full_path_str[:-4]

print("The best fitness obtained is: " + \
    str(best_fit_dict[best_best_fit].get_fitness()) + \
        ";\nObtained for the model with the parameters: " + \
            best_best_fit + ";\nFor the following path: " + \
                full_path_str)
                #str(best_fit_dict[best_best_fit].returnPath()))

