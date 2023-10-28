def up(board, n):
    treasure_found = False
    out_of_bounds = False

    start_index = board.index(1)
    if start_index < n:
        out_of_bounds = True
        return board, out_of_bounds, treasure_found
    else:
        if board[start_index - n] == 2:
            treasure_found = True
        board[start_index - n] = 1
        board[start_index] = 0
        return board, out_of_bounds, treasure_found


def down(board, n):
    treasure_found = False
    out_of_bounds = False

    start_index = board.index(1)
    if start_index >= (n * n) - n:
        out_of_bounds = True
        return board, out_of_bounds, treasure_found
    else:
        if board[start_index + n] == 2:
            treasure_found = True
        board[start_index + n] = 1
        board[start_index] = 0
        return board, out_of_bounds, treasure_found


def left(board, n):
    treasure_found = False
    out_of_bounds = False

    start_index = board.index(1)
    if start_index % n == 0:
        out_of_bounds = True
        return board, out_of_bounds, treasure_found
    else:
        if board[start_index - 1] == 2:
            treasure_found = True
        board[start_index - 1] = 1
        board[start_index] = 0
        return board, out_of_bounds, treasure_found


def right(board, n):
    treasure_found = False
    out_of_bounds = False

    start_index = board.index(1)
    if start_index % n == n - 1:
        out_of_bounds = True
        return board, out_of_bounds, treasure_found
    else:
        if board[start_index + 1] == 2:
            treasure_found = True
        board[start_index + 1] = 1
        board[start_index] = 0
        return board, out_of_bounds, treasure_found
