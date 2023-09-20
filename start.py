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


def start():
    board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    up(board)
    print(board)


start()
