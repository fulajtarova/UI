import random
import printing
import game


def main():
    while True:
        individual_count = int(input("Enter the number of individuals (approx. 20): "))
        random_values_for_individuals = int(
            input(
                "Enter number of random values for individual in virtual machine (approx. 16-64): "
            )
        )
        while random_values_for_individuals > 64:
            print("Invalid number of random values. Please try again.")
            random_values_for_individuals = int(
                input(
                    "Enter number of random values for individual in virtual machine (approx. 16-64): "
                )
            )
        mutation_probability = float(input("Enter the mutation probability: "))
        max_generations = int(input("Enter the maximum number of generations: "))
        user_option = int(
            input(
                "\n1. Generate a board from assignment\n2. Generate a custom board\n3. Exit\n"
            )
        )

        while user_option != 1 and user_option != 2 and user_option != 3:
            print("Invalid option. Please try again.")
            user_option = int(
                input(
                    "\n1. Generate a board from assignment\n2. Generate a custom board\n3. Exit\n"
                )
            )
        print()
        """individual_count = 20
        random_values_for_individuals = 30
        mutation_probability = 0.1
        max_generations = 10
        user_option = 1"""

        if user_option == 3:
            print("Exiting...")
            exit()
        elif user_option == 1:
            treasure_count = 5
            board_size = 7
            board = [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                2,
                0,
                0,
                0,
                0,
                2,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                2,
                0,
                2,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                2,
                0,
                0,
                0,
                0,
                0,
                1,
                0,
                0,
                0,
            ]
            printing.print_letter_board(board)
        else:
            board_size = int(input("Enter the board size: "))

            printing.print_number_board(board_size)

            board = [0] * (board_size * board_size)

            starting_point_index = (
                int(input("Enter number of the starting point: ")) - 1
            )

            while starting_point_index < 0 or starting_point_index >= len(board):
                print("Starting point index is out of bounds. Please correct it.")
                starting_point_index = (
                    int(input("Enter number of the starting point: ")) - 1
                )

            board[starting_point_index] = 1

            treasure_indexes = []
            while True:
                index_input = input(
                    "Enter the treasure indexes (separated by spaces): "
                )
                indexes = index_input.split()

                valid_indexes = True
                for index in indexes:
                    treasure_index = int(index) - 1
                    if treasure_index < 0 or treasure_index >= len(board):
                        print("Treasure index is out of bounds. Please correct it.")
                        valid_indexes = False
                        break

                    if board[treasure_index] == 1:
                        print(
                            "Warning: Treasure is placed on the starting point. Please correct it."
                        )
                        valid_indexes = False
                        break

                if valid_indexes:
                    treasure_indexes = indexes
                    break

            for index in treasure_indexes:
                board[int(index) - 1] = 2

            treasure_count = 0

            for item in board:
                if item == 2:
                    treasure_count += 1

            printing.print_letter_board(board)

        game.play_game(
            board,
            board_size,
            individual_count,
            mutation_probability,
            max_generations,
            treasure_count,
            random_values_for_individuals,
        )


if __name__ == "__main__":
    main()
