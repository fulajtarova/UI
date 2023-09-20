def up(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                if i > 0:
                    board[i][j], board[i - 1][j] = board[i - 1][j], board[i][j]
                break


def down(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                if i < len(board) - 1:
                    board[i][j], board[i + 1][j] = board[i + 1][j], board[i][j]
                break


def left(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                if j > 0:
                    board[i][j], board[i][j - 1] = board[i][j - 1], board[i][j]
                break


def right(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                if j < len(board[i]) - 1:
                    board[i][j], board[i][j + 1] = board[i][j + 1], board[i][j]
                break


def print_board(board):
    for i in board:
        print(i)
    print()


def start():
    board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    up(board)
    print_board(board)
    right(board)
    print_board(board)
    left(board)
    print_board(board)


start()
