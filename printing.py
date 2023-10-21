def print_number_board(n):
    cell_width = len(str(n * n)) + 2  # Calculate the width for each cell

    # Calculate the total width of the board
    board_width = n * (cell_width + 2) + 1

    for i in range(n):
        # Print the top border of the row
        print("+" + "-" * (board_width - 2) + "+")

        # Print the content of the row
        for j in range(n):
            num = i * n + j + 1
            cell = "{:^{width}}".format(num, width=cell_width)
            print("|", cell, end="")

        # End the row with a vertical line
        print("|")

    # Print the bottom border of the board
    print("+" + "-" * (board_width - 2) + "+")


def print_letter_board(board):
    n = int(len(board) ** 0.5)
    cell_width = len(str(n * n)) + 2  # Calculate the width for each cell

    # Calculate the total width of the board
    board_width = n * (cell_width + 2) + 1

    for i in range(n):
        # Print the top border of the row
        print("+" + "-" * (board_width - 2) + "+")

        # Print the content of the row
        for j in range(n):
            num = board[i * n + j]
            if num == 0:
                cell = "{:^{width}}".format(" ", width=cell_width)
            elif num == 1:
                cell = "{:^{width}}".format("S", width=cell_width)
            elif num == 2:
                cell = "{:^{width}}".format("T", width=cell_width)
            print("|", cell, end="")

        # End the row with a vertical line
        print("|")

    # Print the bottom border of the board
    print("+" + "-" * (board_width - 2) + "+")
