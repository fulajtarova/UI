import random
import copy

solution = None


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
        up_child=None,
        down_child=None,
        right_child=None,
        left_child=None,
        parent=None,
        f=None,
    ):
        self.board = board  # The game board
        self.operand = operand  # The move that led to this board (e.g., "up", "down", "right", "left")
        self.depth = depth  # The depth of this node in the tree
        self.f = f
        self.up_child = up_child  # Up child
        self.down_child = down_child  # Down child
        self.right_child = right_child  # Right child
        self.left_child = left_child  # Left child
        self.parent = parent

    def __str__(self):
        return f"Board: {self.board},Operand: {self.operand}, Depth: {self.depth}, F: {self.f}"

    def print_solution(self):
        path = []

        # Traverse up the tree from the current node, collecting operands
        while self.parent is not None:
            path.append(f"Operation: {self.operand}\n{(self.board)}")
            self = self.parent

        # Print the solution path in reverse order

        print("\n\n".join(reversed(path)))

    def format_board(board):
        formatted_board = ""
        for i in range(3):
            row = board[i * 3 : (i + 1) * 3]
            formatted_board += " ".join(map(str, row))
            formatted_board += "\n" if i < 2 else ""
        return formatted_board


# Function to calculate the heuristic value (wrong tiles)
def calculate_heuristic(board, board_end):
    return wrong_tiles(board, board_end)


def insert(node, board_end, max_depth=10):
    empty_tile_index = node.board.index(0)

    comparison = []

    if is_solved(node.board, board_end) or node.depth >= max_depth:
        global solution
        solution = copy.deepcopy(node)
        return node

    # Attempt to add a left child
    if empty_tile_index % 3 > 0 and (
        node.parent is None or node.parent.operand != "right"
    ):
        temp1 = left(node.board)
        comparison.append([temp1, node.depth + calculate_heuristic(temp1, board_end)])
    else:
        comparison.append([None, float("inf")])

    # Attempt to add a right child
    if empty_tile_index % 3 < 2 and (
        node.parent is None or node.parent.operand != "left"
    ):
        temp2 = right(node.board)
        comparison.append([temp2, node.depth + calculate_heuristic(temp2, board_end)])
    else:
        comparison.append([None, float("inf")])

    # Attempt to add an up child
    if empty_tile_index >= 3 and (node.parent is None or node.parent.operand != "down"):
        temp3 = up(node.board)
        comparison.append([temp3, node.depth + calculate_heuristic(temp3, board_end)])
    else:
        comparison.append([None, float("inf")])

    # Attempt to add a down child
    if empty_tile_index < 6 and (node.parent is None or node.parent.operand != "up"):
        temp4 = down(node.board)
        comparison.append([temp4, node.depth + calculate_heuristic(temp4, board_end)])
    else:
        comparison.append([None, float("inf")])

    # print(comparison)

    min_value = min([item[1] for item in comparison], default=float("inf"))

    for i in range(len(comparison)):
        if comparison[i][1] == min_value and comparison[i][0] is not None:
            if i == 0:
                child = Node(
                    comparison[i][0],
                    "left",
                    node.depth + 1,
                    parent=node,
                    f=node.depth + 1 + calculate_heuristic(comparison[i][0], board_end),
                )
                node.left_child = insert(child, board_end, max_depth)
            if i == 1:
                child = Node(
                    comparison[i][0],
                    "right",
                    node.depth + 1,
                    parent=node,
                    f=node.depth + 1 + calculate_heuristic(comparison[i][0], board_end),
                )
                node.right_child = insert(child, board_end, max_depth)
            if i == 2:
                child = Node(
                    comparison[i][0],
                    "up",
                    node.depth + 1,
                    parent=node,
                    f=node.depth + 1 + calculate_heuristic(comparison[i][0], board_end),
                )
                node.up_child = insert(child, board_end, max_depth)
            if i == 3:
                child = Node(
                    comparison[i][0],
                    "down",
                    node.depth + 1,
                    parent=node,
                    f=node.depth + 1 + calculate_heuristic(comparison[i][0], board_end),
                )
                node.down_child = insert(child, board_end, max_depth)

    return node


# main function to test the code
def start():
    # unsovable board
    # board = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    # board_end = [2, 1, 3, 4, 5, 6, 7, 8, 0]

    # same board
    # board = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    # board_end = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    # board = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    # board_end = [1, 2, 3, 4, 5, 6, 0, 7, 8]

    board = [2, 8, 3, 1, 6, 4, 7, 0, 5]
    board_end = [1, 2, 3, 0, 8, 4, 7, 6, 5]

    # board = random_board()
    # board_end = random_board()

    print("Start:")
    print_board(board)
    print("End:")
    print_board(board_end)

    root = Node(board)
    root.f = root.depth + calculate_heuristic(root.board, board_end)

    root = insert(root, board_end, 10)

    solution.print_solution()

    print()


start()
