import random
import printing
import moves


def vm_create_random_values():
    options = [0, 1]
    values_random_list = []
    for i in range(64):
        bin_num = ""
        for j in range(8):
            bin_num += str(random.choice(options))
        values_random_list.append(bin_num)

    return values_random_list


def play_game(
    board,
    board_size,
    individual_count,
    selection_type,
    mutation_probability,
    elitism,
    elitism_count,
    max_generations,
    treasure_count,
):
    board_copy = board.copy()
    virtual_m = vm_create_random_values()
    # board, out_of_bounds, treasure_found = moves.up(board, board_size)
