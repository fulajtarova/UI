import game
from termcolor import colored


def is_valid_board(board, m, n):
    if not all(isinstance(x, int) for x in board):
        return False

    if len(board) != m * n:
        return False

    if len(set(board)) != len(board):
        return False

    if not all(0 <= x < m * n for x in board):
        return False

    return True


def main():
    print(colored("Welcome to the puzzle solver.", "green"))
    while True:
        print("\nDo you want to enter the board or generate a random board?")
        print("Enter 'q' to quit.")
        print("1. Enter the board")
        print("2. Generate a random board")

        choice = input("\nEnter your choice: ")

        if choice == "q":
            break
        elif choice == "1":
            print("Please enter the size of the board!\n")
            m = int(input("Enter the number of rows: "))
            n = int(input("Enter the number of columns: "))

            while True:
                try:
                    board_start = [
                        int(x)
                        for x in input(
                            f"\nEnter the starting board from 0 to {m*n-1}: "
                        )
                    ]
                    board_end = [
                        int(x)
                        for x in input(f"Enter the ending board from 0 to {m*n-1}: ")
                    ]

                    if is_valid_board(board_start, m, n) and is_valid_board(
                        board_end, m, n
                    ):
                        break
                    else:
                        print("\nInvalid input! Please enter the board again!")

                except ValueError:
                    print(
                        "\nInvalid input! Please enter valid integers without spaces."
                    )

            print("Valid input:")
            print(f"Starting board:\n{game.print_board(board_start, m, n)}")
            print(f"\nEnding board:\n{game.print_board(board_end, m, n)}")
        elif choice == "2":
            print("Please enter the size of the board!\n")
            m = int(input("Enter the number of rows: "))
            n = int(input("Enter the number of columns: "))

            board_start = game.random_board(m, n)
            board_end = game.random_board(m, n)
            print("\nRandomly generated boards:")
            print(f"Starting board:\n{game.print_board(board_start, m, n)}")
            print(f"\nEnding board:\n{game.print_board(board_end, m, n)}")
        else:
            print(
                "\nInvalid choice. Please enter '1' to enter the board or '2' to generate a random board."
            )

        print(colored("\nSolving the puzzle...\n", "blue"))
        game.astar(board_start, board_end, n)


if __name__ == "__main__":
    main()
