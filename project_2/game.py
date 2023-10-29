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

    return individual_object


def play_game(
    board,
    board_size,
    individual_count,
    mutation_probability,
    max_generations,
    treasure_count,
    random_values_for_individuals,
):
    for generation in range(max_generations):
        generation_list = []
        for individual in range(individual_count):
            board_copy = board.copy()
            individual_values = vm_create_random_values(random_values_for_individuals)
            individual_object = virtual_machine(
                individual_values, board_copy, board_size, treasure_count
            )
            generation_list.append(individual_object)
