import tkinter as tk
import printing
import time


def start_animation(path, board, board_size, cell_size, canvas):
    for move in path:
        if move == "up":
            board = printing.up(board, board_size)
        elif move == "down":
            board = printing.down(board, board_size)
        elif move == "left":
            board = printing.left(board, board_size)
        elif move == "right":
            board = printing.right(board, board_size)

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
        1000, lambda: start_animation(path, board, board_size, cell_size, canvas)
    )

    animation_duration = 4000 + len(path) * 500
    root.after(animation_duration, root.destroy)
