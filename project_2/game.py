import random
import printing
import moves
from individual import Individual


def vm_create_random_values(n):
    values_random_list = []
    for i in range(n):
        num = "".join(random.choice("01") for _ in range(8))
        values_random_list.append(num)

    for i in range(64 - n):
        values_random_list.append("00000000")

    return values_random_list


def virtual_machine(individual, board, board_size, treasure_count):
    moves_list = []
    out_of_bounds = False
    treasure_found_num = 0
    register_index = 0
    for i in range(500):
        if register_index <= 63:
            opcode = individual[register_index][:2]
            register_value = bin(int(individual[register_index][2:], 2) + 1)[2:]
            if opcode == "00":
                if register_value == "111111":
                    individual[register_index] = "01000000"
                else:
                    register_bin = bin(int(register_value, 2) + 1)[2:].zfill(6)
                    individual[register_index] = opcode + register_bin
                register_index += 1

            elif opcode == "01":
                if register_value == "0":
                    individual[register_index] = "00111111"
                else:
                    register_bin = bin(int(register_value, 2) - 1)[2:].zfill(6)
                    individual[register_index] = opcode + register_bin
                register_index += 1

            elif opcode == "10":
                register_index = int(register_value, 2)

            elif opcode == "11":
                ones_count = individual[i].count("1")
                if ones_count <= 2:
                    board, out_of_bounds, treasure_found = moves.up(board, board_size)
                    if not out_of_bounds:
                        moves_list.append("up")
                elif ones_count <= 4:
                    board, out_of_bounds, treasure_found = moves.down(board, board_size)
                    if not out_of_bounds:
                        moves_list.append("down")
                elif ones_count <= 6:
                    board, out_of_bounds, treasure_found = moves.left(board, board_size)
                    if not out_of_bounds:
                        moves_list.append("left")
                else:
                    board, out_of_bounds, treasure_found = moves.right(
                        board, board_size
                    )
                    if not out_of_bounds:
                        moves_list.append("right")
                if treasure_found:
                    treasure_found_num += 1
        else:
            register_index = 0

        if out_of_bounds or treasure_found_num == treasure_count:
            break

    fitness = treasure_found_num / (len(moves_list) + 1)

    individual_object = Individual(individual, fitness, moves_list)

    solution_found = False
    if treasure_found_num == treasure_count:
        solution_found = True

    return individual_object, solution_found


def mutation(other_generation_list, mutation_probability):
    mutation_list = []
    for individual in other_generation_list:
        if random.random() < mutation_probability:
            individual_values = individual.value
            mutated_individual = []
            for value in individual_values:
                mutated_value = "".join(
                    bit if i % 2 == 0 else "1" if bit == "0" else "0"
                    for i, bit in enumerate(value)
                )
                mutated_individual.append(mutated_value)
            mutation_list.append(mutated_individual)
        else:
            mutation_list.append(individual.value)

    return mutation_list


def make_first_generation(
    board, individual_count, random_values_for_individuals, board_size, treasure_count
):
    generation_list_object = []

    solution_path = None

    for i in range(individual_count):
        board_copy = board.copy()
        individual_values = vm_create_random_values(random_values_for_individuals)
        individual_object, solution_found = virtual_machine(
            individual_values, board_copy, board_size, treasure_count
        )
        generation_list_object.append(individual_object)
        if solution_found:
            solution_path = individual_object.moves_list
            break

    return generation_list_object, solution_path


def crossover(mutation_list):
    crossover_list = []
    for i, individual in enumerate(mutation_list):
        if i == len(mutation_list) - 1:
            parent_1 = mutation_list[i][4:]
            parent_2 = mutation_list[0][:4]
            child = parent_1 + parent_2
            crossover_list.append(child)
        else:
            parent_1 = mutation_list[i][4:]
            parent_2 = mutation_list[i + 1][:4]
            child = parent_1 + parent_2
            crossover_list.append(child)

    return crossover_list


def play_game(
    board,
    board_size,
    individual_count,
    mutation_probability,
    max_generations,
    treasure_count,
    random_values_count_for_individuals,
    elite_individual_count,
):
    solution_found = False

    first_generation_list, solution_path = make_first_generation(
        board,
        individual_count,
        random_values_count_for_individuals,
        board_size,
        treasure_count,
    )

    if solution_path is not None:
        print("Solution found!")
        print("Solution path: ")
        print(solution_path)
        return

    generation_list = first_generation_list

    for generation in range(max_generations - 1):
        if solution_found:
            break

        generation_list.sort(key=lambda x: x.fitness, reverse=True)

        elite_individuals = generation_list[:elite_individual_count]
        other_individuals = generation_list[elite_individual_count:]

        new_generation_list = []
        for individual in elite_individuals:
            new_generation_list.append(individual.value)

        generation_list = new_generation_list

        # mame zmutovanych jedincov
        mutation_list = mutation(other_individuals, mutation_probability)

        # crossover
        crossover_list = crossover(mutation_list)

        # virtual machine for each individual

    if solution_found:
        print("Solution found!")
        print("Solution path: ")
        print(solution_path)
    else:
        print("Solution not found.")
        print("Best individual: ")
        print(generation_list[0].moves_list)
