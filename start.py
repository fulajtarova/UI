import random


# function to move the blank tile up
def up(board):
    for i in range(len(board)):
        if board[i] == 0:
            board[i], board[i - 3] = board[i - 3], board[i]
            return board


# function to move the blank tile down
def down(board):
    for i in range(len(board)):
        if board[i] == 0:
            board[i], board[i + 3] = board[i + 3], board[i]
            return board


# function to move the blank tile left
def left(board):
    for i in range(len(board)):
        if board[i] == 0:
            board[i], board[i - 1] = board[i - 1], board[i]
            return board


# function to move the blank tile to the right
def right(board):
    for i in range(len(board)):
        if board[i] == 0:
            board[i], board[i + 1] = board[i + 1], board[i]
            return board


# function to print the board
def print_board(board):
    for i in range(3):
        row = board[i * 3 : (i + 1) * 3]
        print(" ".join(map(str, row)))
    print()


# function to generate a random board
def random_board():
    numbers = list(range(9))
    random.shuffle(numbers)
    board = [numbers]
    return board[0]


# functoin to check if the board is solved
def is_solved(board, board_end):
    for i in range(len(board)):
        if board[i] != board_end[i]:
            return False
    return True


# heurisric 1
# function to calculate how many tiles are in the wrong position
def wrong_tiles(board, board_end):
    count = 0
    for i in range(len(board)):
        if board[i] != board_end[i] and board[i] != 0:
            count += 1
    return count


# heuristic 2
# Function to calculate the Manhattan distance for a single tile
def manhattan_distance(tile, current_position, goal_position):
    if tile == 0:
        return 0
    tile -= 1
    current_row, current_col = current_position // 3, current_position % 3
    goal_row, goal_col = goal_position // 3, goal_position % 3
    return abs(current_row - goal_row) + abs(current_col - goal_col)


# Function to calculate the sum of Manhattan distances for all tiles
def tiles_distance(board, goal):
    distance = 0
    for i in range(len(board)):
        tile_value = board[i]
        goal_position = goal.index(tile_value)
        distance += manhattan_distance(tile_value, i, goal_position)
    return distance


# function to count inversions
def count_inversions(arr):
    inversions = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inversions += 1
    return inversions


# function to check if the board is solvable
def is_solvable(board_start, board_end):
    inversions_start = count_inversions(board_start)
    inversions_end = count_inversions(board_end)

    return inversions_start % 2 == inversions_end % 2


# function for creating tree with A* algorithm
def create_tree(board, board_end):
    # TODO

    return board


# main function to test the code
def start():
    # unsovable board
    # board = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    # board_end = [2, 1, 3, 4, 5, 6, 7, 8, 0]

    # same board
    # board = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    # board_end = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    board = random_board()
    board_end = random_board()

    print("Start:")
    print_board(board)
    print("End:")
    print_board(board_end)

    print("Is solvable: ")
    print(is_solvable(board, board_end), "\n")

    print("Wrong tiles: ")
    print(wrong_tiles(board, board_end), "\n")

    print("Is solved: ")
    print(is_solved(board, board_end), "\n")

    print("Tiles distance: ")
    print(tiles_distance(board, board_end), "\n")

    # f=g+h g=depth h=heuristic


start()
