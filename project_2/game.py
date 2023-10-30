import random
import moves
from individual import Individual
import copy


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
                register_index += 1
        else:
            register_index = 0

        if out_of_bounds or treasure_found_num == treasure_count:
            break

    # fitness = treasure_found_num / (len(moves_list) + 1)
    fitness = treasure_found_num

    individual_object = Individual(
        individual_copy, fitness, moves_list, treasure_found_num
    )

    solution_found = False
    if treasure_found_num == treasure_count:
        solution_found = True

    return individual_object, solution_found


def mutation(other_generation_list, mutation_probability):
    mutation_list = []
    """
    for individual in other_generation_list:
        mutated_individual = []
        for byte in individual:
            if random.random() < mutation_probability:
                mutated_byte = "".join(random.choice("01") for _ in range(8))
                mutated_individual.append(mutated_byte)
            else:
                mutated_individual.append(byte)
        mutation_list.append(mutated_individual)
    """
    for individual in other_generation_list:
        if random.random() < mutation_probability:
            for j in range(8):  # zmutovane byty v jednom jedinci
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


def crossover(elite_individuals, individual_count, elite_individual_count):
    subelite_individuals = []
    while len(subelite_individuals) != (individual_count - elite_individual_count):
        parent_1 = random.choice(elite_individuals)
        parent_2 = random.choice(elite_individuals)
        while parent_1 == parent_2:
            parent_2 = random.choice(elite_individuals)
        parent_1_values = parent_1.value
        parent_2_values = parent_2.value
        r_num = random.randint(1, 64)
        first_child = parent_1_values[:r_num] + parent_2_values[r_num:]
        second_child = parent_2_values[:r_num] + parent_1_values[r_num:]
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


def make_other_generations(generation_list_values, board, board_size, treasure_count):
    solution_path = None
    generation_list_object = []
    solution_found = False
    for individual in generation_list_values:
        board_copy = board.copy()
        individual_object, solution_found = virtual_machine(
            individual, board_copy, board_size, treasure_count
        )
        generation_list_object.append(individual_object)
        if solution_found:
            solution_path = individual_object.moves_list
            break

    return generation_list_object, solution_path


def tournament(generation_list_object, individual_count):
    potential_parent1 = random.choice(generation_list_object)
    potential_parent2 = random.choice(generation_list_object)
    while potential_parent1 == potential_parent2:
        potential_parent2 = random.choice(generation_list_object)

    potential_parent3 = random.choice(generation_list_object)
    while (
        potential_parent3 == potential_parent1 or potential_parent3 == potential_parent2
    ):
        potential_parent3 = random.choice(generation_list_object)
    potential_parent4 = random.choice(generation_list_object)
    while (
        potential_parent4 == potential_parent1
        or potential_parent4 == potential_parent2
        or potential_parent4 == potential_parent3
    ):
        potential_parent4 = random.choice(generation_list_object)

    if potential_parent1.fitness >= potential_parent2.fitness:
        parent1 = potential_parent1
    else:
        parent1 = potential_parent2

    if potential_parent3.fitness >= potential_parent4.fitness:
        parent2 = potential_parent3
    else:
        parent2 = potential_parent4


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

    board_copy = board.copy()

    first_generation_list, solution_path = make_first_generation(
        board_copy,
        individual_count,
        random_values_count_for_individuals,
        board_size,
        treasure_count,
    )

    generation_list_object = first_generation_list

    if solution_path is not None:
        print("Solution found!")
        print("Solution path: ")
        print(solution_path)
        return

    # for one in range(max_generations):
    for one in range(max_generations):
        if solution_found:
            break

        generation_list_object.sort(key=lambda x: x.fitness, reverse=True)

        print("Generation: ", one + 1)
        for element in generation_list_object:
            print(element.treasure_found_num, element.fitness, element.moves_list)
        print()

        """# vyber najlepsich
        elite_individuals = []
        elite_individuals = copy.deepcopy(generation_list_object[:3])

        other_individuals = []
        other_individuals = copy.deepcopy(generation_list_object[3:])"""
        elite_individuals = []
        elite_individuals = copy.deepcopy(
            generation_list_object[:elite_individual_count]
        )

        """# turnament
        tournament_list = []
        tournament_list = tournament(
            copy.deepcopy(generation_list_object), individual_count
        )"""

        subelite_individuals = []
        subelite_individuals = crossover(
            copy.deepcopy(elite_individuals), individual_count, elite_individual_count
        )

        mutation_list = []
        mutation_list = mutation(subelite_individuals, mutation_probability)

        subelite_list_objects, solution_path = make_other_generations(
            mutation_list, board_copy, board_size, treasure_count
        )
        if solution_path is not None:
            print("Solution found!")
            print("Solution path: ")
            print(solution_path)
            return

        population_list_object = []
        population_list_object = copy.deepcopy(elite_individuals)
        population_list_object.extend(subelite_list_objects)

        generation_list_object = population_list_object

    print("Solution not found.")
    print("Best individual: ")
    print(generation_list_object[0].moves_list)
