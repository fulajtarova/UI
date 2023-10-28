import random
import printing
import moves


def vm_create_random_values(n):
    values_random_list = []
    for i in range(n):
        bin_num = "".join(random.choice("01") for _ in range(8))
        values_random_list.append(bin_num)

    for i in range(64 - n):
        values_random_list.append("00000000")

    return values_random_list


def vm_individual_to_moves(individual):
    moves_list = []
    for i in range(0, 64):
        instruction = individual[i][0:2]
        register = individual[i][2:]
    return moves_list


def play_game(
    board,
    board_size,
    individual_count,
    mutation_probability,
    max_generations,
    treasure_count,
    random_values_for_individuals,
):
    board_copy = board.copy()
    individual = vm_create_random_values(random_values_for_individuals)
    print(individual)
    # board, out_of_bounds, treasure_found = moves.up(board, board_size)
