import time
import game

# colors
Red = "\033[0;31m"
Green = "\033[0;32m"
Orange = "\033[0;33m"
Blue = "\033[0;34m"
Purple = "\033[0;35m"
Cyan = "\033[0;36m"
White = "\033[0;37m"
black = "\033[0;30m"
black = "\033[0;90m"
red = "\033[0;91m"
green = "\033[0;92m"
yellow = "\033[0;93m"
blue = "\033[0;94m"
magenta = "\033[0;95m"
cyan = "\033[0;96m"
white = "\033[0;97m"
cyan_back = "\033[0;46m"
pink_back = "\033[0;45m"
white_back = "\033[0;47m"
blue_back = "\033[0;44m"
orange_back = "\033[0;43m"
green_back = "\033[0;42m"
red_back = "\033[0;41m"
grey_back = "\033[0;40m"
bold = "\033[1m"
underline = "\033[4m"
italic = "\033[3m"
darken = "\033[2m"
reset = "\033[0m"


def is_valid_board(board, n):
    if not all(isinstance(x, int) for x in board):
        return False

    if len(board) != n * n:
        return False

    if len(set(board)) != len(board):
        return False

    if not all(0 <= x < n * n for x in board):
        return False

    return True


def main():
    print(pink_back + "Welcome to the puzzle solver." + reset)
    while True:
        print(
            green
            + "\nDo you want to enter the board or generate a random board?"
            + reset
        )
        print("Enter 'q' to quit.")
        print("1. Enter the board")
        print("2. Generate a random board")

        choice = input("\nEnter your choice: ")

        if choice == "q":
            print("\nThank you for playing! Leaving the game...")
            break
        elif choice == "1":
            n = int(input("Enter the number of rows and columns: "))

            while True:
                try:
                    board_start = [
                        int(x)
                        for x in input(
                            f"\nEnter the starting board (space-separated) from 0 to {n*n-1}: "
                        ).split()
                    ]
                    board_end = [
                        int(x)
                        for x in input(
                            f"Enter the ending board (space-separated) from 0 to {n*n-1}: "
                        ).split()
                    ]

                    if is_valid_board(board_start, n) and is_valid_board(board_end, n):
                        break
                    else:
                        print("\nInvalid input! Please enter the board again!")

                except ValueError:
                    print(
                        "\nInvalid input! Please enter valid integers separated by spaces."
                    )

            print(cyan + "\nBoards:" + reset)
            print(f"Starting board:\n{game.print_board(board_start, n)}")
            print(f"\nEnding board:\n{game.print_board(board_end, n)}")
        elif choice == "2":
            n = int(input("Enter the number of columns: "))

            board_start = game.random_board(n)
            board_end = game.random_board(n)
            print(cyan + "\nRandomly generated boards:" + reset)
            print(f"Starting board:\n{game.print_board(board_start, n)}")
            print(f"\nEnding board:\n{game.print_board(board_end,  n)}")
        else:
            print(
                "\nInvalid choice. Please enter '1' to enter the board or '2' to generate a random board."
            )

        board_start1 = board_start.copy()
        board_start2 = board_start.copy()

        print(blue + "\nSolving the puzzle with 1. heuristic-wrong tiles...\n" + reset)
        t10 = time.time()
        game.astar(board_start1, board_end, n, 1)
        t11 = time.time()
        t1f = t11 - t10

        print(
            blue
            + "\nSolving the puzzle with 2. heuristic-manhattan distance...\n"
            + reset
        )

        t20 = time.time()
        game.astar(board_start2, board_end, n, 2)
        t21 = time.time()
        t2f = t21 - t20

        if game.get_num_of_moves(1) != 0 and game.get_num_of_moves(2) != 0:
            print(magenta + "\n\nComparing the two heuristics:" + reset)

            print(f"\nTime taken for heuristic-wrong tiles: {round(t1f*1000,3)} ms")
            print(
                f"Time taken for heuristic-manhattan distance: {round(t2f*1000,3)} ms"
            )

            print(
                f"\nNumber of steps for heuristic-wrong tiles: {game.get_num_of_moves(1)}"
            )
            print(
                f"Number of steps for heuristic-manhattan distance: {game.get_num_of_moves(2)}",
            )

            if t1f < t2f:
                print(
                    f"\nHeuristic-wrong tiles is faster than heuristic-manhattan distance"
                )
            elif t1f > t2f:
                print(
                    f"\nHeuristic-manhattan distance is faster than heuristic-wrong tiles"
                )
            else:
                print(
                    f"\nHeuristic-wrong tiles and heuristic-manhattan distance take the same time"
                )

            if game.get_num_of_moves(1) < game.get_num_of_moves(2):
                print(
                    f"Heuristic-wrong tiles takes {game.get_num_of_moves(2) - game.get_num_of_moves(1)} more steps than heuristic-manhattan distance"
                )
            elif game.get_num_of_moves(1) > game.get_num_of_moves(2):
                print(
                    f"Heuristic-manhattan distance takes {game.get_num_of_moves(1) - game.get_num_of_moves(2)} more steps than heuristic-wrong tiles"
                )
            else:
                print(
                    f"Heuristic-wrong tiles and heuristic-manhattan distance take the same number of steps"
                )
        elif game.get_num_of_moves(1) == 0 and game.get_num_of_moves(2) != 0:
            print(magenta + "\n\nComparing the two heuristics:" + reset)
            print("\nHeuristic-wrong tiles was not able to find a solution")
            print(
                f"\nTime taken for heuristic-manhattan distance: {round(t2f*1000,3)} ms"
            )
            print(
                f"Number of steps for heuristic-manhattan distance: {game.get_num_of_moves(2)}",
            )
        elif game.get_num_of_moves(2) == 0 and game.get_num_of_moves(1) != 0:
            print(magenta + "\n\nComparing the two heuristics:" + reset)
            print("\nHeuristic-manhattan distance was not able to find a solution")
            print(f"\nTime taken for heuristic-wrong tiles: {round(t1f*1000,3)} ms")
            print(
                f"Number of steps for heuristic-wrong tiles: {game.get_num_of_moves(1)}"
            )

        else:
            print(Orange + "\nNo solution found in either case" + reset)


if __name__ == "__main__":
    main()

# 123045678
# 012345678

# 123804765

# 567408321 start
# 123804765 end
