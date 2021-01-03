import state


def misplaced_heuristic(state):
    misplaced_count = 0
    for i in range(len(state.board)):
        for j in range(len(state.board[i])):
            if state.board[i][j] != i * len(state.board[i]) + j and state.board[i][j] != 0:
                misplaced_count += 1
    return misplaced_count


def manhattan_heuristic(state, tile_subset=None):
    if tile_subset is None:
        tile_subset = set(range(1, state.n ** 2))
    moves_count = 0
    for i in range(len(state.board)):
        for j in range(len(state.board[i])):
            cell = state.board[i][j]
            if cell in tile_subset:
                i_goal = cell // len(state.board[i])
                j_goal = cell % len(state.board[i])
                moves_count += abs(i - i_goal) + abs(j - j_goal)
    return moves_count


def linear_conflicts_heuristic(state):
    moves_count = manhattan_heuristic(state)

    # row linear conflicts
    for i in range(len(state.board)):
        correct_row_elements = []
        for j in range(len(state.board[i])):
            cell = state.board[i][j]
            if cell != 0:
                i_goal = cell // len(state.board[i])
                if i == i_goal:
                    correct_row_elements.append(cell)
        while correct_row_elements:
            min_cell = min(correct_row_elements)
            if correct_row_elements[0] != min_cell:
                moves_count += 2
            correct_row_elements.remove(min_cell)

    # column linear conflicts
    for j in range(len(state.board[0])):
        correct_column_elements = []
        for i in range(len(state.board)):
            cell = state.board[i][j]
            if cell != 0:
                j_goal = cell % len(state.board[i])
                if j == j_goal:
                    correct_column_elements.append(cell)
        while correct_column_elements:
            min_cell = min(correct_column_elements)
            if correct_column_elements[0] != min_cell:
                moves_count += 2
            correct_column_elements.remove(min_cell)

    return moves_count


def linear_conflicts_subset_heuristic(state, subset):
    moves_count = manhattan_heuristic(state, subset)

    # row linear conflicts
    for i in range(len(state.board)):
        correct_row_elements = []
        for j in range(len(state.board[i])):
            cell = state.board[i][j]
            if cell in subset:
                i_goal = cell // len(state.board[i])
                if i == i_goal:
                    correct_row_elements.append(cell)
        while correct_row_elements:
            min_cell = min(correct_row_elements)
            if correct_row_elements[0] != min_cell:
                moves_count += 2
            correct_row_elements.remove(min_cell)

    # column linear conflicts
    for j in range(len(state.board[0])):
        correct_column_elements = []
        for i in range(len(state.board)):
            cell = state.board[i][j]
            if cell in subset:
                j_goal = cell % len(state.board[i])
                if j == j_goal:
                    correct_column_elements.append(cell)
        while correct_column_elements:
            min_cell = min(correct_column_elements)
            if correct_column_elements[0] != min_cell:
                moves_count += 2
            correct_column_elements.remove(min_cell)

    return moves_count


def disjoint_database_heuristic(state_, subsets, databases):
    h = 0
    for i in range(len(subsets)):
        substate = state.SBPSubstate(state_.n, subsets[i], state_.board)
        h += databases[i][repr(substate)]
    return h


def disjoint_database_reflection_heuristic(state_, subsets, databases):
    reflected_board = []
    for i in range(state_.n):
        reflected_board.append([])
        for j in range(state_.n):
            cell = state_.board[j][i]
            i1 = cell//state_.n
            j1 = cell%state_.n
            cell1 = j1*state_.n+i1
            reflected_board[i].append(cell1)
    reflected_state = state.SBPState(state_.n, reflected_board)
    return max(disjoint_database_heuristic(state_, subsets, databases),
               disjoint_database_heuristic(reflected_state, subsets, databases))
