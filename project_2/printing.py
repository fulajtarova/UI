import matplotlib.pyplot as plt
import tkinter as tk


def print_number_board(n):
    cell_width = len(str(n * n)) + 2

    board_width = n * (cell_width + 2) + 1

    for i in range(n):
        print("+" + "-" * (board_width - 2) + "+")

        for j in range(n):
            num = i * n + j + 1
            cell = "{:^{width}}".format(num, width=cell_width)
            print("|", cell, end="")

        print("|")

    print("+" + "-" * (board_width - 2) + "+")
    print("\n")


def print_letter_board(board):
    n = int(len(board) ** 0.5)
    cell_width = len(str(n * n)) + 2

    board_width = n * (cell_width + 2) + 1

    for i in range(n):
        print("+" + "-" * (board_width - 2) + "+")

        for j in range(n):
            num = board[i * n + j]
            if num == 0:
                cell = "{:^{width}}".format(" ", width=cell_width)
            elif num == 1:
                cell = "{:^{width}}".format("S", width=cell_width)
            elif num == 2:
                cell = "{:^{width}}".format("T", width=cell_width)
            print("|", cell, end="")

        print("|")

    print("+" + "-" * (board_width - 2) + "+")
    print("\n")


def up(board, n):
    start_index = board.index(1)
    board[start_index - n] = 1
    board[start_index] = 3
    return board


def down(board, n):
    start_index = board.index(1)
    board[start_index + n] = 1
    board[start_index] = 3
    return board


def left(board, n):
    start_index = board.index(1)
    board[start_index - 1] = 1
    board[start_index] = 3
    return board


def right(board, n):
    start_index = board.index(1)
    board[start_index + 1] = 1
    board[start_index] = 3
    return board


def graph(generation_fitness_list):
    x = range(1, len(generation_fitness_list) + 1)
    plt.bar(x, generation_fitness_list)

    plt.xlabel("Generation")
    plt.ylabel("Fitness")

    plt.show()


def start_animation(path, board, board_size, cell_size, canvas):
    for move in path:
        if move == "up":
            board = up(board, board_size)
        elif move == "down":
            board = down(board, board_size)
        elif move == "left":
            board = left(board, board_size)
        elif move == "right":
            board = right(board, board_size)

        for row in range(board_size):
            for col in range(board_size):
                x0 = col * cell_size
                y0 = row * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                cell_value = board[row * board_size + col]

                if cell_value == 0:
                    canvas.create_rectangle(x0, y0, x1, y1, fill="white")
                elif cell_value == 1:
                    canvas.create_rectangle(x0, y0, x1, y1, fill="magenta")
                elif cell_value == 2:
                    canvas.create_rectangle(x0, y0, x1, y1, fill="gold")
                else:
                    canvas.create_rectangle(x0, y0, x1, y1, fill="pink")

        canvas.update()
        canvas.after(500)


def animation(board, board_size, path):
    cell_size = 50

    canvas_width = board_size * cell_size
    canvas_height = board_size * cell_size

    root = tk.Tk()
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    canvas.after(
        500, lambda: start_animation(path, board, board_size, cell_size, canvas)
    )
