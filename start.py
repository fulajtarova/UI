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


# Function to create the A* search tree
def a_star_recursive(board_start, board_end):
    start_node = Node(board_start)
    start_node.heuristic = calculate_heuristic(start_node.board, board_end)

    open_list = [start_node]
    closed_set = set()

    while open_list:
        current_node = min(open_list, key=lambda node: node.depth + node.heuristic)
        open_list.remove(current_node)

        if current_node.board == board_end:
            return current_node

        closed_set.add(tuple(current_node.board))

        empty_tile_index = current_node.board.index(0)
        possible_moves = []

        if empty_tile_index % 3 > 0:
            possible_moves.append(("left", -1))
        if empty_tile_index % 3 < 2:
            possible_moves.append(("right", 1))
        if empty_tile_index >= 3:
            possible_moves.append(("up", -3))
        if empty_tile_index < 6:
            possible_moves.append(("down", 3))

        for move, move_offset in possible_moves:
            new_board = current_node.board[:]
            new_board[empty_tile_index], new_board[empty_tile_index + move_offset] = (
                new_board[empty_tile_index + move_offset],
                new_board[empty_tile_index],
            )
            new_node = Node(
                new_board,
                operation=move,
                depth=current_node.depth + 1,
                parent=current_node,
            )
            new_node.heuristic = calculate_heuristic(new_node.board, board_end)

            if tuple(new_node.board) not in closed_set:
                open_list.append(new_node)

    return None


class Node:
    def __init__(self, board, operation=None, depth=0, parent=None):
        self.board = board
        self.operation = operation
        self.depth = depth
        self.parent = parent
        self.heuristic = 0

    def __lt__(self, other):
        return (self.depth + self.heuristic) < (other.depth + other.heuristic)


# Function to calculate the heuristic value (wrong tiles)
def calculate_heuristic(board, board_end):
    return wrong_tiles(board, board_end)


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

    while is_solvable(board, board_end) == False:
        board = random_board()
        board_end = random_board()

    print("Start:")
    print_board(board)
    print("End:")
    print_board(board_end)

    solution_node = a_star_recursive(board, board_end)

    if solution_node:
        print("Solution path:")
        path = []
        current_node = solution_node
        while current_node:
            path.append(current_node)
            current_node = current_node.parent
        path.reverse()
        for node in path:
            print_board(node.board)
            print("Operation:", node.operation)
            print("Depth:", node.depth)
            print("Heuristic:", node.heuristic)
            print()
    else:
        print("No solution found.")


# f=g+h g=depth h=heuristic


start()
