import printing
import moves


def mainos():
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

    postupnost = [
        "left",
        "up",
        "left",
        "up",
        "right",
        "up",
        "right",
        "down",
        "up",
        "right",
        "up",
        "left",
        "down",
        "up",
        "right",
        "up",
        "right",
        "down",
        "up",
        "right",
        "up",
        "left",
        "down",
        "down",
        "right",
        "up",
        "left",
        "down",
        "left",
        "right",
        "up",
        "left",
        "down",
        "down",
        "right",
        "up",
        "right",
        "down",
        "left",
        "right",
        "up",
        "left",
        "down",
        "left",
        "right",
        "up",
        "left",
        "down",
        "up",
        "right",
        "up",
        "left",
        "down",
        "down",
        "right",
        "up",
        "left",
        "down",
        "left",
        "right",
        "up",
        "left",
        "down",
        "left",
        "right",
        "up",
        "left",
        "down",
        "down",
        "right",
        "up",
        "down",
        "down",
        "left",
        "right",
        "up",
        "right",
        "down",
    ]

    for i in postupnost:
        if i == "up":
            board, out_of_bounds, treasure_found = moves.up(board, 7)
        elif i == "down":
            board, out_of_bounds, treasure_found = moves.down(board, 7)
        elif i == "left":
            board, out_of_bounds, treasure_found = moves.left(board, 7)
        elif i == "right":
            board, out_of_bounds, treasure_found = moves.right(board, 7)

    printing.print_letter_board(board)


mainos()
