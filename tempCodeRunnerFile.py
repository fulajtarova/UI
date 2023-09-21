current_board, depth, f_value = solution
        while current_board != board:
            print_board(current_board)
            print("Depth:", depth)
            print("f-value:", f_value)
            print()
            current_board, depth, f_value = a_star(current_board, board_end)
        print_board(board)
        print("Depth:", depth)
        print("f-value:", f_value)