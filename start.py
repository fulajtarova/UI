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


# function to calculate how many tiles are in the wrong position
def wrong_tiles(board, board_end):
    count = 0
    for i in range(len(board)):
        if board[i] != board_end[i] and board[i] != 0:
            count += 1
    return count


"""


"""


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
    # board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    # board_end = [[2, 1, 3], [4, 5, 6], [7, 8, 0]]

    main_board = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    # board = random_board(main_board)
    # board_end = random_board(main_board)

    board = [2, 8, 3, 1, 6, 4, 7, 0, 5]
    board_end = [1, 2, 3, 8, 0, 4, 7, 6, 5]

    print("Start:")
    print_board(board)
    print("End:")
    print_board(board_end)

    print("Wrong tiles: ")
    print(wrong_tiles(board, board_end))

    """
    print("Is solvable: ")
    print(is_solvable(board, board_end))

    print("Is solved: ")
    print(is_solved(board, board_end))

    
    print("Tiles distance: ")
    print(tiles_distance(board, board_end))"""

    # f=g+h g=depth h=heuristic


start()
