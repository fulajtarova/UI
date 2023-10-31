import random
import moves
from individual import Individual
import copy
import printing
import move_animation


def vm_create_random_values(n):
    values_random_list = []

    for _ in range(n):
        num = "".join(random.choice("01") for _ in range(8))
        values_random_list.append(num)

    random.shuffle(values_random_list)

    for i in range(64 - n):
        values_random_list.append("00000000")

    return values_random_list


def virtual_machine(individual, board, board_size, treasure_count):
    board_copy = board.copy()
    moves_list = []
    individual_copy = individual.copy()
    out_of_bounds = False
    treasure_found_num = 0
    register_index = 0
    for i in range(500):
        if register_index <= 63:
            opcode = individual[register_index][:2]
            register_value = individual[register_index][2:]
            if opcode == "00":
                new_register_index = int(register_value, 2)
                new_register_value = individual[new_register_index]
                if new_register_value == "11111111":
                    individual[register_index] = "00000000"
                else:
                    register_bin = bin(int(new_register_value, 2) + 1)[2:]
                    individual[new_register_index] = register_bin.zfill(8)
                register_index += 1

            elif opcode == "01":
                new_register_index = int(register_value, 2)
                new_register_value = individual[new_register_index]
                if new_register_value == "00000000":
                    individual[register_index] = "11111111"
                else:
                    register_bin = bin(int(new_register_value, 2) - 1)[2:]
                    individual[new_register_index] = register_bin.zfill(8)
                register_index += 1

            elif opcode == "10":
                register_index = int(register_value, 2)

            elif opcode == "11":
                new_register_index = int(register_value, 2)
                new_register_value = individual[new_register_index]
                ones_count = new_register_value.count("1")
                if ones_count <= 2:
                    board_copy, out_of_bounds, treasure_found = moves.up(
                        board_copy, board_size
                    )
                    if not out_of_bounds:
                        moves_list.append("up")
                elif ones_count <= 4:
                    board_copy, out_of_bounds, treasure_found = moves.down(
                        board_copy, board_size
                    )
                    if not out_of_bounds:
                        moves_list.append("down")
                elif ones_count <= 6:
                    board_copy, out_of_bounds, treasure_found = moves.left(
                        board_copy, board_size
                    )
                    if not out_of_bounds:
                        moves_list.append("left")
                else:
                    board_copy, out_of_bounds, treasure_found = moves.right(
                        board_copy, board_size
                    )
                    if not out_of_bounds:
                        moves_list.append("right")
                if treasure_found:
                    treasure_found_num += 1
                register_index += 1
        else:
            register_index = 0
        if out_of_bounds or treasure_found_num == treasure_count:
            break

    # fitness = treasure_found_num / (len(moves_list) + 1)
    fitness = treasure_found_num

    individual_object = Individual(
        individual_copy, fitness, moves_list, treasure_found_num, board_copy
    )

    if treasure_found_num == treasure_count:
        global solution_individual
        solution_individual = individual_object

    return individual_object


def mutation(other_generation_list, mutation_probability):
    mutation_list = []
    for individual in other_generation_list:
        for j in range(mutation_probability):  # zmutovane byty v jednom jedinci
            cell_index = random.randint(0, 63)
            cell = individual[cell_index]
            dec_byte = int(cell, 2)
            for k in range(3):  # zmutovane bity v jednom byte
                mask = 1 << random.randint(0, 7)
                cell = dec_byte ^ mask
                dec_byte = cell
            individual[cell_index] = bin(cell)[2:].zfill(8)
        mutation_list.append(individual)

    return mutation_list


def crossover(parent1, parent2):
    r_num = random.randint(1, 64)
    first_child = parent1[:r_num] + parent2[r_num:]
    second_child = parent2[:r_num] + parent1[r_num:]
    return first_child, second_child


def roulette_wheel(generation_list_object, individual_count, elite_individual_count):
    subelite_individuals = []

    total_fitness = sum(individual.fitness for individual in generation_list_object)

    selection_probabilities = [
        individual.fitness / total_fitness for individual in generation_list_object
    ]

    while len(subelite_individuals) != (individual_count - elite_individual_count):
        parent1 = random.choices(generation_list_object, selection_probabilities)[0]
        parent2 = random.choices(generation_list_object, selection_probabilities)[0]

        first_child, second_child = crossover(parent1.value, parent2.value)

        if first_child not in subelite_individuals and len(
            subelite_individuals
        ) + 1 <= (individual_count - elite_individual_count):
            subelite_individuals.append(first_child)
        if second_child not in subelite_individuals and len(
            subelite_individuals
        ) + 1 <= (individual_count - elite_individual_count):
            subelite_individuals.append(second_child)

    return subelite_individuals


def tournament_winner(generation_list_object, size_of_tournament):
    tournament_list = []
    for _ in range(size_of_tournament):
        tournament_list.append(random.choice(generation_list_object))
    tournament_list.sort(key=lambda x: x.fitness, reverse=True)
    winner = tournament_list[0]
    return winner


def tournament(generation_list_object, individual_count, elite_individual_count):
    subelite_individuals = []
    size_of_tournament = random.randint(2, 5)
    while len(subelite_individuals) != (individual_count - elite_individual_count):
        parent_1 = tournament_winner(generation_list_object, size_of_tournament)
        parent_2 = tournament_winner(generation_list_object, size_of_tournament)

        while parent_1 == parent_2:
            parent_2 = tournament_winner(generation_list_object, size_of_tournament)

        parent_1_values = parent_1.value
        parent_2_values = parent_2.value

        first_child, second_child = crossover(parent_1_values, parent_2_values)

        if first_child not in subelite_individuals and len(
            subelite_individuals
        ) + 1 <= (individual_count - elite_individual_count):
            subelite_individuals.append(first_child)
        if second_child not in subelite_individuals and len(
            subelite_individuals
        ) + 1 <= (individual_count - elite_individual_count):
            subelite_individuals.append(second_child)

    return subelite_individuals


def make_first_generation(
    board, individual_count, random_values_for_individuals, board_size, treasure_count
):
    generation_list_object = []

    global solution_individual

    for i in range(individual_count):
        if solution_individual is None:
            board_copy = board.copy()
            individual_values = vm_create_random_values(random_values_for_individuals)
            individual_object = virtual_machine(
                individual_values, board_copy, board_size, treasure_count
            )
            generation_list_object.append(individual_object)

    return generation_list_object


def make_other_generations(generation_list_values, board, board_size, treasure_count):
    generation_list_object = []

    global solution_individual
    for individual in generation_list_values:
        if solution_individual is None:
            board_copy = board.copy()
            individual_object = virtual_machine(
                individual, board_copy, board_size, treasure_count
            )
            generation_list_object.append(individual_object)

    return generation_list_object


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
    global solution_individual
    solution_individual = None

    board_copy = board.copy()

    first_generation_list = make_first_generation(
        board_copy,
        individual_count,
        random_values_count_for_individuals,
        board_size,
        treasure_count,
    )

    generation_list_object = first_generation_list

    best_fintness_generations = []

    global generation_num
    generation_num = 1

    # for one in range(max_generations):
    while solution_individual is None and generation_num < max_generations:
        generation_num += 1
        generation_list_object.sort(key=lambda x: x.fitness, reverse=True)

        best_fintness_generations.append(generation_list_object[0].fitness)

        elite_individuals = []
        elite_individuals = copy.deepcopy(
            generation_list_object[:elite_individual_count]
        )

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

        mutation_list = []
        mutation_list = mutation(subelite_individuals, mutation_probability)

        subelite_list_objects = make_other_generations(
            mutation_list, board_copy, board_size, treasure_count
        )

        population_list_object = []
        population_list_object = copy.deepcopy(elite_individuals)
        population_list_object.extend(subelite_list_objects)

        generation_list_object = population_list_object

    print(len(best_fintness_generations))

    if solution_individual is not None:
        print("\nSolution found.")
        print(f"\nGeneration number: {generation_num}")
        print("Solution path: ")
        print(solution_individual.moves_list)
        best_fintness_generations.append(solution_individual.fitness)
        printing.graph(best_fintness_generations)
        print("Solution board: ")
        printing.print_letter_board(solution_individual.board)
        if animation == 1:
            move_animation.animation(
                board_copy, board_size, solution_individual.moves_list
            )

    else:
        print("\nSolution not found.")
        print(f"Generation number: {generation_num}")
        print("Best solution path: ")
        print(generation_list_object[0].moves_list)
        best_fintness_generations.append(generation_list_object[0].fitness)
        printing.graph(best_fintness_generations)
        print("Best solution board: ")
        printing.print_letter_board(generation_list_object[0].board)
