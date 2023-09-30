import heapq
import random
import copy

solution = None

"""
------------------------------------------------------------------------------------------------------------------------
"""


# Function to move the blank tile up
def up(board, n):
    board_copy = copy.deepcopy(board)
    for i in range(len(board_copy)):
        if board_copy[i] == 0:
            if i - n >= 0:  # Check if moving up is within bounds
                board_copy[i], board_copy[i - n] = board_copy[i - n], board_copy[i]
                return board_copy
    return board_copy


# Function to move the blank tile down
def down(board, n):
    board_copy = copy.deepcopy(board)
    for i in range(len(board_copy)):
        if board_copy[i] == 0:
            if i + n < len(board_copy):  # Check if moving down is within bounds
                board_copy[i], board_copy[i + n] = board_copy[i + n], board_copy[i]
                return board_copy
    return board_copy


# Function to move the blank tile left
def left(board, n):
    board_copy = copy.deepcopy(board)
    for i in range(len(board_copy)):
        if board_copy[i] == 0:
            if i % n != 0:  # Check if moving left is within bounds
                board_copy[i], board_copy[i - 1] = board_copy[i - 1], board_copy[i]
                return board_copy
    return board_copy


# Function to move the blank tile to the right
def right(board, n):
    board_copy = copy.deepcopy(board)
    for i in range(len(board_copy)):
        if board_copy[i] == 0:
            if (i + 1) % n != 0:  # Check if moving right is within bounds
                board_copy[i], board_copy[i + 1] = board_copy[i + 1], board_copy[i]
                return board_copy
    return board_copy


"""
------------------------------------------------------------------------------------------------------------------------
"""


# function to print the board
def print_board(board, m, n):
    new_board = ""
    for i in range(m):
        for j in range(n):
            new_board += f"{board[i*n+j]:2d} "
        new_board += "\n"

    return new_board


"""
------------------------------------------------------------------------------------------------------------------------
"""


# function to generate a random board
def random_board(m, n):
    numbers = list(range(m * n))
    random.shuffle(numbers)
    board = [numbers]
    return board[0]


"""
------------------------------------------------------------------------------------------------------------------------
"""


# functoin to check if the board is solved
def is_same(board, board_end):
    return board == board_end


"""
------------------------------------------------------------------------------------------------------------------------
"""


# heurisric 1
# function to calculate how many tiles are in the wrong position
def heuristic_1_wrong_tiles(board, board_end):
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
def heuristic_2_tiles_distance(board, goal):
    distance = 0
    for i in range(len(board)):
        tile_value = board[i]
        goal_position = goal.index(tile_value)
        distance += manhattan_distance(tile_value, i, goal_position)
    return distance


"""
------------------------------------------------------------------------------------------------------------------------
"""


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

    # Define a custom comparison method for nodes
    def __lt__(self, other):
        return self.f < other.f


"""
------------------------------------------------------------------------------------------------------------------------
"""


def calculate_heuristic(board, board_end):
    return heuristic_1_wrong_tiles(board, board_end)


"""
------------------------------------------------------------------------------------------------------------------------
"""

# Initialize a set for the closed list
closed_set = set()


# Function to insert child nodes into the open list
def insert(node, board_end, open_list, n, max_depth=50):
    if is_same(node.board, board_end) or node.depth >= max_depth:
        global solution
        solution = copy.deepcopy(node)
        print("Solution found!")
        return None

    # Check if the node's board configuration is already in the closed set
    if tuple(node.board) in closed_set:
        return node  # Skip this node if it's in the closed set

    # Add the current board configuration to the closed set
    closed_set.add(tuple(node.board))

    l_ch = left(node.board, n)
    r_ch = right(node.board, n)
    u_ch = up(node.board, n)
    d_ch = down(node.board, n)

    if not is_same(l_ch, node.board):
        child = Node(
            l_ch,
            "left",
            node.depth + 1,
            parent=node,
            f=node.depth + 1 + calculate_heuristic(l_ch, board_end),
        )
        if child.board not in open_list:
            heapq.heappush(open_list, (child.f, child))

    if not is_same(r_ch, node.board):
        child = Node(
            r_ch,
            "right",
            node.depth + 1,
            parent=node,
            f=node.depth + 1 + calculate_heuristic(r_ch, board_end),
        )
        if child.board not in open_list:
            heapq.heappush(open_list, (child.f, child))

    if not is_same(u_ch, node.board):
        child = Node(
            u_ch,
            "up",
            node.depth + 1,
            parent=node,
            f=node.depth + 1 + calculate_heuristic(u_ch, board_end),
        )
        if child.board not in open_list:
            heapq.heappush(open_list, (child.f, child))

    if not is_same(d_ch, node.board):
        child = Node(
            d_ch,
            "down",
            node.depth + 1,
            parent=node,
            f=node.depth + 1 + calculate_heuristic(d_ch, board_end),
        )
        if child.board not in open_list:
            heapq.heappush(open_list, (child.f, child))

    return node


# Start of A* Algorithm
def astar(board_start, board_end, n):
    global solution
    start_node = Node(board_start)
    solution = None
    open_list = []
    heapq.heappush(open_list, (start_node.f, start_node))
    while open_list:
        _, current_node = heapq.heappop(open_list)
        insert(current_node, board_end, open_list, n, 50)
        if solution:
            break

    if solution:
        print_solution_path(solution)


# Rest of the code remains the same


# Function to print the solution path
def print_solution_path(solution_node):
    path = []
    current_node = solution_node
    while current_node:
        if current_node.operand:
            path.append(current_node.operand)
        current_node = current_node.parent

    path.reverse()
    print("Solution Path:")
    for move in path:
        print(move)
