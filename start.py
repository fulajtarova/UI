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


# Function to create the A* search tree
def a_star(node, board_end, heuristic_threshold=float("inf")):
    empty_tile_index = node.board.index(0)
    # has a left child
    if empty_tile_index % 3 > 0:
        left_board = left(node.board)
        left_heuristic = calculate_heuristic(left_board, board_end)
        if left_heuristic <= heuristic_threshold:
            node.left = Node(left_board)
            node.left.heuristic = left_heuristic
            node.left.depth = node.depth + 1
    # has a right child
    if empty_tile_index % 3 < 2:
        right_board = right(node.board)
        right_heuristic = calculate_heuristic(right_board, board_end)
        if right_heuristic <= heuristic_threshold:
            node.right = Node(right_board)
            node.right.heuristic = right_heuristic
            node.right.depth = node.depth + 1
    # has an up child
    if empty_tile_index >= 3:
        up_board = up(node.board)
        up_heuristic = calculate_heuristic(up_board, board_end)
        if up_heuristic <= heuristic_threshold:
            node.up = Node(up_board)
            node.up.heuristic = up_heuristic
            node.up.depth = node.depth + 1
    # has a down child
    if empty_tile_index < 6:
        down_board = down(node.board)
        down_heuristic = calculate_heuristic(down_board, board_end)
        if down_heuristic <= heuristic_threshold:
            node.down = Node(down_board)
            node.down.heuristic = down_heuristic
            node.down.depth = node.depth + 1

    return node


"""
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
"""


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

    for item in comparison:
        if item[1] == min_value:
            child = Node(board=item[0], operand=None, depth=node.depth + 1, parent=node)
            node.l_child = insert(child, board_end, max_depth)
            break

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
    board_end = [1, 2, 3, 4, 5, 6, 7, 0, 8]

    # board = random_board()
    # board_end = random_board()

    print("Start:")
    print_board(board)
    print("End:")
    print_board(board_end)

    """node = Node(board)

    while is_solved(node.board, board_end) == False:
        node = a_star(node, board_end)"""

    root = Node(board)
    root.f = root.depth + calculate_heuristic(root.board, board_end)
    print(root)

    root = insert(root, board_end, 10)

    """
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
        print("No solution found.")"""


start()
