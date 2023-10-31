import random
import copy

from individual import Individual
import moves
import printing

# colors
Orange = "\033[0;33m"
green = "\033[0;92m"
blue = "\033[0;94m"
magenta = "\033[0;95m"
cyan = "\033[0;96m"
pink_back = "\033[0;45m"
reset = "\033[0m"


"""
------------------------------------------------------------------------------------------------------------------------
    This function creates random values for the virtual machine.
    The values are 8-bit binary numbers.
------------------------------------------------------------------------------------------------------------------------
"""


def vm_create_random_values(n):
    values_random_list = []

    # we create n random 8-bit binary numbers and add them to the list
    for _ in range(n):
        num = "".join(random.choice("01") for _ in range(8))
        values_random_list.append(num)

    for i in range(64 - n):
        values_random_list.append("00000000")

    return values_random_list


"""
------------------------------------------------------------------------------------------------------------------------
    This function is the virtual machine.
    It takes an individual, a board, the board size and the number of treasures as parameters.
    It creates an individual object and returns it.
------------------------------------------------------------------------------------------------------------------------
"""


def virtual_machine(individual, board, board_size, treasure_count):
    board_copy = board.copy()
    moves_list = []
    individual_copy = individual.copy()
    out_of_bounds = False
    treasure_found_num = 0
    register_index = 0

    # loop for 500 cycles and then break
    for i in range(500):
        # if we are at the end of the virtual machine, we start from the beginning
        if register_index <= 63:
            opcode = individual[register_index][:2]
            register_value = individual[register_index][2:]

            # if the opcode is 00, we increment the value on which the register points
            if opcode == "00":
                new_register_index = int(register_value, 2)
                new_register_value = individual[new_register_index]
                if new_register_value == "11111111":
                    individual[register_index] = "00000000"
                else:
                    register_bin = bin(int(new_register_value, 2) + 1)[2:]
                    individual[new_register_index] = register_bin.zfill(8)
                register_index += 1

            # if the opcode is 01, we decrement the value on which the register points
            elif opcode == "01":
                new_register_index = int(register_value, 2)
                new_register_value = individual[new_register_index]
                if new_register_value == "00000000":
                    individual[register_index] = "11111111"
                else:
                    register_bin = bin(int(new_register_value, 2) - 1)[2:]
                    individual[new_register_index] = register_bin.zfill(8)
                register_index += 1

            # if the opcode is 10, we move the register to the register on which it points
            elif opcode == "10":
                register_index = int(register_value, 2)

            # if the opcode is 11, we add moves to the moves list based on the value of the register on which it points
            elif opcode == "11":
                new_register_index = int(register_value, 2)
                new_register_value = individual[new_register_index]
                ones_count = new_register_value.count("1")
                # if it has got 0 or 1 ones, we move up
                if ones_count <= 2:
                    board_copy, out_of_bounds, treasure_found = moves.up(
                        board_copy, board_size
                    )
                    if not out_of_bounds:
                        moves_list.append("up")
                # if it has got 2 or 3 ones, we move down
                elif ones_count <= 4:
                    board_copy, out_of_bounds, treasure_found = moves.down(
                        board_copy, board_size
                    )
                    if not out_of_bounds:
                        moves_list.append("down")
                # if it has got 4 or 5 ones, we move left
                elif ones_count <= 6:
                    board_copy, out_of_bounds, treasure_found = moves.left(
                        board_copy, board_size
                    )
                    if not out_of_bounds:
                        moves_list.append("left")
                # if it has got 6 or 7 ones, we move right
                else:
                    board_copy, out_of_bounds, treasure_found = moves.right(
                        board_copy, board_size
                    )
                    if not out_of_bounds:
                        moves_list.append("right")

                # if we found a treasure, we increment the treasure_found_num
                if treasure_found:
                    treasure_found_num += 1
                register_index += 1
        else:
            register_index = 0

        # if we are out of bounds or we found all the treasures, we break
        if out_of_bounds or treasure_found_num == treasure_count:
            break

    # we calculate the fitness of the individual
    fitness = 2 / (len(moves_list) + 1) + 5 * treasure_found_num

    # we create an individual object
    individual_object = Individual(
        individual_copy, fitness, moves_list, treasure_found_num, board_copy
    )

    # if we found all the treasures, we save the individual as the solution
    if treasure_found_num == treasure_count:
        global solution_individual
        solution_individual = individual_object

    return individual_object


"""
------------------------------------------------------------------------------------------------------------------------
    This function mutates the individuals.
    It returns a list of mutated individuals.
    We mutate the individuals by changing 3 random bits in a random cell based on the mutation probability.
------------------------------------------------------------------------------------------------------------------------
"""


def mutation(other_generation_list, mutation_probability):
    mutation_list = []

    # we loop through the individuals in the other generation list and its cells
    for individual in other_generation_list:
        for j in range(mutation_probability):
            # we choose a random cell and change 3 random bits in it with a mask
            cell_index = random.randint(0, 63)
            cell = individual[cell_index]
            dec_byte = int(cell, 2)
            for k in range(3):
                mask = 1 << random.randint(0, 7)
                cell = dec_byte ^ mask
                dec_byte = cell
            individual[cell_index] = bin(cell)[2:].zfill(8)
        mutation_list.append(individual)

    return mutation_list


"""
------------------------------------------------------------------------------------------------------------------------
    This function performs crossover between two individuals in a random point.
    It returns two children created by the crossover.
------------------------------------------------------------------------------------------------------------------------
"""


def crossover(parent1, parent2):
    # we choose a random point and create two children by combining the parents
    r_num = random.randint(1, 64)
    first_child = parent1[:r_num] + parent2[r_num:]
    second_child = parent2[:r_num] + parent1[r_num:]
    return first_child, second_child


"""
------------------------------------------------------------------------------------------------------------------------
    This function performs roulette wheel selection.
    It creates a list of selection probabilities based on the fitness of the individuals.
    It selects two parents based on the selection probabilities.
    It returns a list of subelite individuals.
------------------------------------------------------------------------------------------------------------------------
"""


def roulette_wheel(generation_list_object, individual_count, elite_individual_count):
    subelite_individuals = []

    # we calculate the total fitness of the individuals
    total_fitness = sum(individual.fitness for individual in generation_list_object)

    # we create a list of selection probabilities based on the fitness of the individuals
    selection_probabilities = [
        individual.fitness / total_fitness for individual in generation_list_object
    ]

    # we add individuals to the subelite list until we reach the desired number of individuals
    while len(subelite_individuals) != (individual_count - elite_individual_count):
        # we choose two parents based on the selection probabilities
        parent1 = random.choices(generation_list_object, selection_probabilities)[0]
        parent2 = random.choices(generation_list_object, selection_probabilities)[0]

        # we do crossover between the two parents and create two children
        first_child, second_child = crossover(parent1.value, parent2.value)

        # we add the children to the subelite list if they are not already in it
        if first_child not in subelite_individuals and len(
            subelite_individuals
        ) + 1 <= (individual_count - elite_individual_count):
            subelite_individuals.append(first_child)
        if second_child not in subelite_individuals and len(
            subelite_individuals
        ) + 1 <= (individual_count - elite_individual_count):
            subelite_individuals.append(second_child)

    return subelite_individuals


"""
------------------------------------------------------------------------------------------------------------------------
    This functions performs tournament selection.
    It creates a random sized tournament list.
    It selects two parents based on the fitness of the individuals in the tournament list.
    Winner of the tournament is the individual with the highest fitness and it becomes a parent.
    It creates two children by performing crossover between the two parents.
    It returns a list of subelite individuals.
------------------------------------------------------------------------------------------------------------------------
"""


def tournament_winner(generation_list_object, size_of_tournament):
    tournament_list = []

    # we create a random sized tournament list and select a winner
    for _ in range(size_of_tournament):
        tournament_list.append(random.choice(generation_list_object))
    tournament_list.sort(key=lambda x: x.fitness, reverse=True)
    winner = tournament_list[0]
    return winner


def tournament(generation_list_object, individual_count, elite_individual_count):
    subelite_individuals = []

    # we create random sized tournaments until we reach the desired number of individuals
    size_of_tournament = random.randint(2, 5)
    while len(subelite_individuals) != (individual_count - elite_individual_count):
        # parents are selected based on the fitness of the individuals in the tournament list
        parent_1 = tournament_winner(generation_list_object, size_of_tournament)
        parent_2 = tournament_winner(generation_list_object, size_of_tournament)

        # we make sure that the two parents are not the same
        while parent_1 == parent_2:
            parent_2 = tournament_winner(generation_list_object, size_of_tournament)

        # we do crossover between the two parents and create two children
        parent_1_values = parent_1.value
        parent_2_values = parent_2.value

        first_child, second_child = crossover(parent_1_values, parent_2_values)

        # we add the children to the subelite list if they are not already in it
        if first_child not in subelite_individuals and len(
            subelite_individuals
        ) + 1 <= (individual_count - elite_individual_count):
            subelite_individuals.append(first_child)
        if second_child not in subelite_individuals and len(
            subelite_individuals
        ) + 1 <= (individual_count - elite_individual_count):
            subelite_individuals.append(second_child)

    return subelite_individuals


"""
------------------------------------------------------------------------------------------------------------------------
    This function creates the first generation.
    It randomly creates values for the individuals.
    It run the virtual machine for each individual.
    It returns a list of individual objects.
------------------------------------------------------------------------------------------------------------------------
"""


def make_first_generation(
    board, individual_count, random_values_for_individuals, board_size, treasure_count
):
    generation_list_object = []
    global solution_individual

    for i in range(individual_count):
        if solution_individual is None:
            board_copy = board.copy()
            # we create random values for the virtual machine and run it for each individual
            individual_values = vm_create_random_values(random_values_for_individuals)
            individual_object = virtual_machine(
                individual_values, board_copy, board_size, treasure_count
            )
            # objects are added to the list
            generation_list_object.append(individual_object)

    return generation_list_object


"""
------------------------------------------------------------------------------------------------------------------------
    This function creates the other generations.
    It run the virtual machine for each individual.
    It returns a list of individual objects.
------------------------------------------------------------------------------------------------------------------------
"""


def make_other_generations(generation_list_values, board, board_size, treasure_count):
    generation_list_object = []

    global solution_individual
    for individual in generation_list_values:
        if solution_individual is None:
            board_copy = board.copy()
            # we run the virtual machine for each individual
            individual_object = virtual_machine(
                individual, board_copy, board_size, treasure_count
            )
            # objects are added to the list
            generation_list_object.append(individual_object)

    return generation_list_object


"""
------------------------------------------------------------------------------------------------------------------------
    This function is the main function of the game.
    It loops until the solution is found or the maximum number of generations is reached.
    It sorts the individuals based on their fitness.
    It selects the elite individuals and puts them in a list to be used in the next generation.
    It selects the subelite individuals based on the selection type and does crossover between them and mutates them.
    It creates the next generation by combining the elite and subelite individuals.
    It prints the solution if it is found, otherwise it prints the best solution.
------------------------------------------------------------------------------------------------------------------------
"""


def play_game(
    board,
    board_size,
    individual_count,
    mutation_probability,
    max_generations,
    treasure_count,
    random_values_count_for_individuals,
    elite_individual_count,
    selection_type,
    animation,
):
    # we initialize the solution so we can use it in other functions and stop the game if it is found, and the generation number
    global solution_individual, generation_num
    solution_individual = None
    board_copy = board.copy()
    best_fintness_individuals = []
    generation_num = 1

    # we create the first generation
    first_generation_list = make_first_generation(
        board_copy,
        individual_count,
        random_values_count_for_individuals,
        board_size,
        treasure_count,
    )

    # first generation is our current generation
    generation_list_object = first_generation_list

    # we loop until the solution is found or the maximum number of generations is reached
    while solution_individual is None and generation_num < max_generations:
        generation_num += 1

        # we sort the individuals based on their fitness
        generation_list_object.sort(key=lambda x: x.fitness, reverse=True)

        # best fitness is added to the list for the graph at the end of the game
        best_fintness_individuals.append(generation_list_object[0].fitness)

        # copy of the elite individuals
        elite_individuals = []
        elite_individuals = copy.deepcopy(
            generation_list_object[:elite_individual_count]
        )

        # based on the selection type, we select the subelite individuals by roulette wheel or tournament and do crossover between them
        subelite_individuals = []
        if selection_type == 1:
            subelite_individuals = roulette_wheel(
                copy.deepcopy(generation_list_object),
                individual_count,
                elite_individual_count,
            )
        else:
            subelite_individuals = tournament(
                copy.deepcopy(generation_list_object),
                individual_count,
                elite_individual_count,
            )

        # we mutate the subelite individuals
        mutation_list = []
        mutation_list = mutation(subelite_individuals, mutation_probability)

        # objects are created for the next generation
        subelite_list_objects = make_other_generations(
            mutation_list, board_copy, board_size, treasure_count
        )

        # we combine the elite and subelite individuals to create the next generation
        population_list_object = []
        population_list_object = copy.deepcopy(elite_individuals)
        population_list_object.extend(subelite_list_objects)

        generation_list_object = population_list_object

    # we print the solution if it is found, otherwise we print the best solution
    if solution_individual is not None:
        print(green + "\nSolution found." + reset)
        print(f"Generation number: {generation_num}")
        print(magenta + "Solution path: " + reset)
        print(solution_individual.moves_list)
        best_fintness_individuals.append(solution_individual.fitness)
        printing.graph(best_fintness_individuals)
        print("Solution board after moves: ")
        printing.print_letter_board(solution_individual.board)
        if animation == 1:
            printing.animation(board_copy, board_size, solution_individual.moves_list)

    else:
        print(blue + "\nSolution not found." + reset)
        print(f"Generation number: {generation_num}")
        print(magenta + "Best solution path: " + reset)
        print(generation_list_object[0].moves_list)
        best_fintness_individuals.append(generation_list_object[0].fitness)
        printing.graph(best_fintness_individuals)
        print("Best solution board after moves: ")
        printing.print_letter_board(generation_list_object[0].board)
        if animation == 1:
            printing.animation(
                board_copy, board_size, generation_list_object[0].moves_list
            )
