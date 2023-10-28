import random
import printing
import moves


def vm_create_random_values(n):
    values_random_list = []
    for i in range(n):
        num = "".join(random.choice("01") for _ in range(8))
        values_random_list.append(num)

    for i in range(64 - n):
        values_random_list.append("00000000")

    return values_random_list


def vm_individual_to_moves(individual, board, board_size):
    moves_list = []
    instruction_count = 0
    out_of_bounds = False
    treasure_found = False
    for i, instruction in enumerate(individual):
        opcode = instruction[:2]
        register = bin(int(instruction[2:], 2))[2:]
        if opcode == "00":
            instruction_count += 1
            if register == "111111":
                individual[i] = "00000000"
            else:
                register_bin = bin(int(register, 2) + 1)[2:].zfill(6)
                whole_register = opcode + register_bin
                individual[i] = whole_register
        elif opcode == "01":
            instruction_count += 1
            if register == "0":
                individual[i] = "01111111"
            else:
                register_bin = bin(int(register, 2) - 1)[2:].zfill(6)
                whole_register = opcode + register_bin
                individual[i] = whole_register
        elif opcode == "10":
            instruction_count += 1
            jump_index = int(register, 2)
            # Jump (execute the register)
        elif opcode == "11":
            instruction_count += 1
            ones_count = instruction.count("1")
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
                board, out_of_bounds, treasure_found = moves.right(board, board_size)
                if not out_of_bounds:
                    moves_list.append("right")

        if out_of_bounds or treasure_found or instruction_count > 500:
            break

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
    for individual in range(individual_count):
        board_copy = board.copy()
        individual_values = vm_create_random_values(random_values_for_individuals)
        print(individual_values)
        individual_moves = vm_individual_to_moves(
            individual_values, board_copy, board_size
        )
        print(individual_moves)
