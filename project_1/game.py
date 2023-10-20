import heapq
import random
import copy

solution = None
num_of_moves_h1 = 0
num_of_moves_h2 = 0
num_of_nodes_h1 = 0
num_of_nodes_h2 = 0

"""
------------------------------------------------------------------------------------------------------------------------
Methods to rotate the board 
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
Methods to print the board
------------------------------------------------------------------------------------------------------------------------
"""


# function to print the board
def print_board(board, n):
    new_board = ""
    for i in range(n):
        for j in range(n):
            new_board += f"{board[i*n+j]:2d} "
        new_board += "\n"

    return new_board


"""
------------------------------------------------------------------------------------------------------------------------
Method to generate a random board
------------------------------------------------------------------------------------------------------------------------
"""


# function to generate a random board
def random_board(n):
    numbers = list(range(n * n))
    random.shuffle(numbers)
    board = [numbers]
    return board[0]


"""
------------------------------------------------------------------------------------------------------------------------
Method to check if the board is solved
------------------------------------------------------------------------------------------------------------------------
"""


# functoin to check if the board is solved
def is_same(board, board_end):
    return board == board_end


"""
------------------------------------------------------------------------------------------------------------------------
Methods to calculate the heuristic values for the board configurations 
------------------------------------------------------------------------------------------------------------------------
"""


# heuristic 1
# function to calculate how many tiles are in the wrong position
def heuristic_1_wrong_tiles(board, board_end):
    count = 0
    for i in range(len(board)):
        if board[i] != board_end[i] and board[i] != 0:
            count += 1
    return count


# heuristic 2
# Function to calculate the Manhattan distance for a single tile
def manhattan_distance(tile, current_position, goal_position, n):
    if tile == 0:
        return 0
    current_row, current_col = current_position // n, current_position % n
    goal_row, goal_col = goal_position // n, goal_position % n
    return abs(current_row - goal_row) + abs(current_col - goal_col)


# Function to calculate the sum of Manhattan distances for all tiles
def heuristic_2_tiles_distance(board, goal, n):
    distance = 0
    for i in range(len(board)):
        tile_value = board[i]
        goal_position = goal.index(tile_value)
        distance += manhattan_distance(tile_value, i, goal_position, n)
    return distance


"""
------------------------------------------------------------------------------------------------------------------------
Node class that contains the board configuration, the move that led to this board, the depth of this node and the f value
------------------------------------------------------------------------------------------------------------------------
"""


class Node:
    def __init__(
        self,
        board=[],
        operand=None,
        depth=0,
        parent=None,
        f=None,
    ):
        self.board = board  # The game board
        self.operand = operand  # The move that led to this board (e.g., "up", "down", "right", "left")
        self.depth = depth  # The depth of this node in the tree
        self.f = f  # The estimated cost of this node
        self.parent = parent  # The parent node

    # Define a custom comparison method for nodes
    def __lt__(self, other):
        return self.f < other.f


"""
------------------------------------------------------------------------------------------------------------------------
Method to calculate the heuristic value based on the choice 
------------------------------------------------------------------------------------------------------------------------
"""


def calculate_heuristic(choice, board, board_end, n):
    if choice == 1:
        return heuristic_1_wrong_tiles(board, board_end)
    elif choice == 2:
        return heuristic_2_tiles_distance(board, board_end, n)


"""
------------------------------------------------------------------------------------------------------------------------
A* Algorithm function with methods to insert child nodes into the open list
------------------------------------------------------------------------------------------------------------------------
"""


# Function to insert child nodes into the open list
def insert(node, board_end, open_list, n, choice):
    # Check if the current node's board configuration is the same as the goal board configuration
    # If it is, then we have found the solution and we can stop the search
    if is_same(node.board, board_end):
        global solution
        solution = copy.deepcopy(node)
        return None

    # Check if the node's board configuration is already in the closed set
    if tuple(node.board) in closed_set:
        return node  # Skip this node if it's in the closed set

    # Add the current board configuration to the closed set
    closed_set.add(tuple(node.board))

    # Generate possible child nodes by moving in different directions (left, right, up, down)
    l_ch = left(node.board, n)
    r_ch = right(node.board, n)
    u_ch = up(node.board, n)
    d_ch = down(node.board, n)

    # Check if moving left is a valid move and not the same as the parent
    if not is_same(l_ch, node.board):
        # Create a child node with the new board configuration, depth, parent and f value
        child = Node(
            l_ch,
            "left",
            node.depth + 1,
            parent=node,
            f=node.depth + 1 + calculate_heuristic(choice, l_ch, board_end, n),
        )
        # Check if the child's board configuration is not in the open list
        if child.board not in open_list:
            heapq.heappush(open_list, (child.f, child))

    # Check if moving right is a valid move and not the same as the parent
    if not is_same(r_ch, node.board):
        # Create a child node with the new board configuration, depth, parent and f value
        child = Node(
            r_ch,
            "right",
            node.depth + 1,
            parent=node,
            f=node.depth + 1 + calculate_heuristic(choice, r_ch, board_end, n),
        )
        # Check if the child's board configuration is not in the open list
        if child.board not in open_list:
            heapq.heappush(open_list, (child.f, child))

    # Check if moving up is a valid move and not the same as the parent
    if not is_same(u_ch, node.board):
        # Create a child node with the new board configuration, depth, parent and f value
        child = Node(
            u_ch,
            "up",
            node.depth + 1,
            parent=node,
            f=node.depth + 1 + calculate_heuristic(choice, u_ch, board_end, n),
        )
        # Check if the child's board configuration is not in the open list
        if child.board not in open_list:
            heapq.heappush(open_list, (child.f, child))
    # Check if moving down is a valid move and not the same as the parent
    if not is_same(d_ch, node.board):
        # Create a child node with the new board configuration, depth, parent and f value
        child = Node(
            d_ch,
            "down",
            node.depth + 1,
            parent=node,
            f=node.depth + 1 + calculate_heuristic(choice, d_ch, board_end, n),
        )
        # Check if the child's board configuration is not in the open list
        if child.board not in open_list:
            heapq.heappush(open_list, (child.f, child))

    return node


# Start of A* Algorithm
def astar(board_start, board_end, n, choice):
    # Reset the closed set and solution for each new A* search
    global closed_set, solution, num_of_moves_h1, num_of_moves_h2, num_of_nodes_h1, num_of_nodes_h2
    closed_set = set()
    solution = None

    # Initialize the starting node with the given board configuration
    start_node = Node(board_start)

    # Create an empty priority queue (open list)
    open_list = []

    # Initialize the node count for limiting and stopping the search if it takes too long
    node_count = 0

    # Push the starting node onto the open list with its estimated cost (f)
    heapq.heappush(open_list, (start_node.f, start_node))

    # Main A* search loop
    while open_list:
        # Pop the node with the lowest estimated cost (f) from the open list
        _, current_node = heapq.heappop(open_list)

        # Increment the node count
        node_count += 1

        # Limit the search to 50000 nodes and stop if it takes too long
        if node_count >= 50000:
            print("Reached 50000 nodes, exiting...")
            if choice == 1:
                num_of_moves_h1 = 0
            elif choice == 2:
                num_of_moves_h2 = 0
            break

        # Insert child nodes into the open list and check for the solution
        insert(current_node, board_end, open_list, n, choice)

        # If a solution is found, print the solution path and break out of the loop
        if solution:
            if choice == 1:
                num_of_nodes_h1 = node_count
            elif choice == 2:
                num_of_nodes_h2 = node_count
            print_solution_path(solution, choice)
            break


"""
------------------------------------------------------------------------------------------------------------------------
Method to print the solution path
------------------------------------------------------------------------------------------------------------------------
"""


# Function to print the solution path
def print_solution_path(solution_node, choice):
    i = 0
    path = []
    current_node = solution_node
    # Traverse the tree from the solution node to the root node
    # and append the moves with board configuration to the path list in reverse order
    while current_node:
        if current_node.operand:
            i += 1
            move = current_node.operand
            board = current_node.board
            path.append((move, board))
        current_node = current_node.parent

    path.reverse()

    # Print the solution path in the correct order with the move number, move and board configuration
    print("Solution Path:")
    for i in range(len(path)):
        print(f"Move: {i + 1:<8} {path[i][0]:<10} {path[i][1]}")

    # Update the number of moves for the heuristic choice
    global num_of_moves_h1, num_of_moves_h2

    if choice == 1:
        num_of_moves_h1 = i + 1
    elif choice == 2:
        num_of_moves_h2 = i + 1


"""
------------------------------------------------------------------------------------------------------------------------
Method to get the number of moves and nodes for the heuristic choice for comparison
------------------------------------------------------------------------------------------------------------------------
"""


def get_num_of_moves(choice):
    if choice == 1:
        return num_of_moves_h1
    elif choice == 2:
        return num_of_moves_h2


def get_num_of_nodes(choice):
    if choice == 1:
        return num_of_nodes_h1
    elif choice == 2:
        return num_of_nodes_h2
