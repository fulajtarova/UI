import random
import copy


# Function to move the blank tile up
def up(board):
    board_copy = copy.deepcopy(board)
    for i in range(len(board_copy)):
        if board_copy[i] == 0:
            board_copy[i], board_copy[i - 3] = board_copy[i - 3], board_copy[i]
            return board_copy


# Function to move the blank tile down
def down(board):
    board_copy = copy.deepcopy(board)
    for i in range(len(board_copy)):
        if board_copy[i] == 0:
            board_copy[i], board_copy[i + 3] = board_copy[i + 3], board_copy[i]
            return board_copy


# Function to move the blank tile left
def left(board):
    board_copy = copy.deepcopy(board)
    for i in range(len(board_copy)):
        if board_copy[i] == 0:
            board_copy[i], board_copy[i - 1] = board_copy[i - 1], board_copy[i]
            return board_copy


# Function to move the blank tile to the right
def right(board):
    board_copy = copy.deepcopy(board)
    for i in range(len(board_copy)):
        if board_copy[i] == 0:
            board_copy[i], board_copy[i + 1] = board_copy[i + 1], board_copy[i]
            return board_copy


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


class Node:
    def __init__(
        self,
        board=[],
        operand=None,
        depth=0,
        u_child=None,
        d_child=None,
        r_child=None,
        l_child=None,
        parent=None,
    ):
        self.board = board  # The game board
        self.operand = operand  # The move that led to this board (e.g., "up", "down", "right", "left")
        self.depth = depth  # The depth of this node in the tree
        self.f = None
        self.u_child = u_child  # Up child
        self.d_child = d_child  # Down child
        self.r_child = r_child  # Right child
        self.l_child = l_child  # Left child
        self.parent = parent

    def __str__(self):
        return f"Board: {self.board},Operand: {self.operand}, Depth: {self.depth}, F: {self.f}"

    def print_solution(self):
        path = []
        current_node = self

        while current_node:
            if current_node.operand:
                path.append(current_node.operand)
            current_node = current_node.parent

        path.reverse()
        print("Solution path:")
        print(" -> ".join(path))


# Function to calculate the heuristic value (wrong tiles)
def calculate_heuristic(board, board_end):
    return wrong_tiles(board, board_end)


def insert(node, board_end, max_depth=10):
    empty_tile_index = node.board.index(0)

    comparison = []

    if is_solved(node.board, board_end) or node.depth >= max_depth:
        return node

    # Attempt to add a left child
    if empty_tile_index % 3 > 0 and (
        node.parent is None or node.parent.operand != "right"
    ):
        temp1 = left(node.board)
        comparison.append([temp1, node.depth + calculate_heuristic(temp1, board_end)])

    # Attempt to add a right child
    if empty_tile_index % 3 < 2 and (
        node.parent is None or node.parent.operand != "left"
    ):
        temp2 = right(node.board)
        comparison.append([temp2, node.depth + calculate_heuristic(temp2, board_end)])

    # Attempt to add an up child
    if empty_tile_index >= 3 and (node.parent is None or node.parent.operand != "down"):
        temp3 = up(node.board)
        comparison.append([temp3, node.depth + calculate_heuristic(temp3, board_end)])

    # Attempt to add a down child
    if empty_tile_index < 6 and (node.parent is None or node.parent.operand != "up"):
        temp4 = down(node.board)
        comparison.append([temp4, node.depth + calculate_heuristic(temp4, board_end)])

    print(comparison)

    min_value = min([item[1] for item in comparison], default=float("inf"))
    print(min_value)

    for i in range(len(comparison)):
        if comparison[i] and comparison[i][1] == min_value:
            move_operands = ["left", "right", "up", "down"]
            child_operand = move_operands[i]

            child = Node(
                board=comparison[i][0],
                operand=child_operand,
                depth=node.depth + 1,
                parent=node,
            )

            # Set the correct child attribute based on the operand
            setattr(node, f"{child_operand}_child", insert(child, board_end, max_depth))

    return node


# main function to test the code
def start():
    # unsovable board
    # board = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    # board_end = [2, 1, 3, 4, 5, 6, 7, 8, 0]

    # same board
    # board = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    # board_end = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    board = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    board_end = [1, 2, 3, 4, 5, 6, 0, 7, 8]

    # board = random_board()
    # board_end = random_board()

    print("Start:")
    print_board(board)
    print("End:")
    print_board(board_end)

    root = Node(board)
    root.f = root.depth + calculate_heuristic(root.board, board_end)
    print(root)

    root = insert(root, board_end, 10)

    print(root)


start()
