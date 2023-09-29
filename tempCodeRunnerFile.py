def insert(node, board_end, max_depth=10):
    empty_tile_index = node.board.index(0)

    comparison = []
    visited_positions.add(
        tuple(node.board)
    )  # Add the current board to visited positions

    if is_solved(node.board, board_end) or node.depth >= max_depth:
        global solution
        solution = copy.deepcopy(node)
        return node

    # Attempt to add a left child
    if empty_tile_index % 3 > 0 and (node.parent is None or node.operand != "right"):
        temp1 = left(node.board)
        if tuple(temp1) not in visited_positions:
            comparison.append(
                [temp1, node.depth + calculate_heuristic(temp1, board_end)]
            )
    else:
        comparison.append([None, float("inf")])

    # Attempt to add a right child
    if empty_tile_index % 3 < 2 and (node.parent is None or node.operand != "left"):
        temp2 = right(node.board)
        if tuple(temp2) not in visited_positions:
            comparison.append(
                [temp2, node.depth + calculate_heuristic(temp2, board_end)]
            )
    else:
        comparison.append([None, float("inf")])

    # Attempt to add an up child
    if empty_tile_index >= 3 and (node.parent is None or node.operand != "down"):
        temp3 = up(node.board)
        if tuple(temp3) not in visited_positions:
            comparison.append(
                [temp3, node.depth + calculate_heuristic(temp3, board_end)]
            )
    else:
        comparison.append([None, float("inf")])

    # Attempt to add a down child
    if empty_tile_index < 6 and (node.parent is None or node.operand != "up"):
        temp4 = down(node.board)
        if tuple(temp4) not in visited_positions:
            comparison.append(
                [temp4, node.depth + calculate_heuristic(temp4, board_end)]
            )
    else:
        comparison.append([None, float("inf")])

    print(comparison)

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
