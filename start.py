import random


# function to move the blank tile up
def up(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                if i > 0:
                    board[i][j], board[i - 1][j] = board[i - 1][j], board[i][j]
                return board


# function to move the blank tile down
def down(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                if i < len(board) - 1:
                    board[i][j], board[i + 1][j] = board[i + 1][j], board[i][j]
                return board


# function to move the blank tile left
def left(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                if j > 0:
                    board[i][j], board[i][j - 1] = board[i][j - 1], board[i][j]
                return board


# function to move the blank tile to the right
def right(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                if j < len(board[i]) - 1:
                    board[i][j], board[i][j + 1] = board[i][j + 1], board[i][j]
                return board


# function to print the board
def print_board(board):
    for i in board:
        print(i)
    print()


# function to generate a random board
def random_board(board):
    numbers = list(range(9))
    random.shuffle(numbers)
    board = [[numbers.pop() for _ in range(3)] for _ in range(3)]
    return board


# function to calculate how many tiles are in the wrong position
def wrong_tiles(board, board_end):
    count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != board_end[i][j]:
                count += 1
    return count


# Function to calculate sum of distances of tiles from their goal positions
def tiles_distance(board, board_end):
    distance = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            tile_value = board[i][j]
            goal_i, goal_j = find_goal_position(tile_value, board_end)
            distance += abs(i - goal_i) + abs(j - goal_j)
    return distance


# Function to find the goal position of a tile
def find_goal_position(tile_value, board_end):
    for i, row in enumerate(board_end):
        if tile_value in row:
            j = row.index(tile_value)
            return i, j


# functoin to check if the board is solved
def is_solved(board, board_end):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != board_end[i][j]:
                return False
    return True


# main function to test the code
def start():
    # main_board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    # board = random_board(board)
    # board_end = random_board(board)
    board = [[5, 7, 2], [3, 8, 1], [6, 0, 4]]
    board_end = [[5, 7, 2], [3, 8, 1], [6, 0, 4]]

    # board_end = [[6, 0, 3], [2, 5, 1], [7, 8, 4]]
    print_board(board)
    # print_board(board_end)

    print(wrong_tiles(board, board_end))
    tiles_distance(board, board_end)

    board = right(board)
    print_board(board)

    print(is_solved(board, board_end))


start()
