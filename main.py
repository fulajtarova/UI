import game


def is_valid_board(board, m, n):
    # Check if the input is a list of integers
    if not all(isinstance(x, int) for x in board):
        return False

    # Check if the input has exactly m*n elements
    if len(board) != m * n:
        return False

    # Check if each number in the board is unique within the board
    if len(set(board)) != len(board):
        return False

    # Check if the input contains numbers in the range [0, m*n-1]
    if not all(0 <= x < m * n for x in board):
        return False

    return True


def main():
    print("Welcome to the puzzle solver. Please enter the size of the board!\n")
    m = int(input("Enter the number of rows: "))
    n = int(input("Enter the number of columns: "))

    print("\nDo you want to enter the board or generate a random board?")
    print("1. Enter the board")
    print("2. Generate a random board")
    choice = int(input("\nEnter your choice: "))

    if choice == 1:
        while True:
            try:
                board_start = [
                    int(x)
                    for x in input(f"\nEnter the starting board from 0 to {m*n-1}: ")
                ]
                board_end = [
                    int(x) for x in input(f"Enter the ending board from 0 to {m*n-1}: ")
                ]

                if is_valid_board(board_start, m, n) and is_valid_board(
                    board_end, m, n
                ):
                    break
                else:
                    print("\nInvalid input! Please enter the board again!")

            except ValueError:
                print("\nInvalid input! Please enter valid integers without spaces.")

        print("Valid input:")
        print(f"Starting board:\n{game.print_board(board_start, m, n)}")
        print(f"\nEnding board:\n{game.print_board(board_end, m, n)}")

    elif choice == 2:
        board_start = game.random_board(m, n)
        board_end = game.random_board(m, n)
        print("\nRandomly generated boards:")
        print(f"Starting board:\n{game.print_board(board_start, m, n)}")
        print(f"\nEnding board:\n{game.print_board(board_end, m, n)}")


if __name__ == "__main__":
    main()
