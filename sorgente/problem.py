from copy import deepcopy

import state


class SBPProblem:
    moves = {"left": (0, -1), "right": (0, 1), "up": (-1, 0), "down": (1, 0)}

    def __init__(self, initial_state):
        self.initial_state = initial_state

    @staticmethod
    def actions(state):
        action_set = {"left", "right", "up", "down"}
        i, j = state.find_blank()
        if j == 0:
            action_set.remove("left")
        elif j == len(state.board[i]) - 1:
            action_set.remove("right")
        if i == 0:
            action_set.remove("up")
        elif i == len(state.board) - 1:
            action_set.remove("down")
        return action_set

    @staticmethod
    def result(state, action):
        assert action in SBPProblem.actions(state)
        result_state = deepcopy(state)
        di, dj = SBPProblem.moves[action]
        i, j = state.find_blank()
        result_state.board[i][j], result_state.board[i + di][j + dj] = state.board[i + di][j + dj], state.board[i][j]
        return result_state

    @staticmethod
    def goal_test(state):
        for i in range(len(state.board)):
            for j in range(len(state.board[i])):
                if state.board[i][j] != i * len(state.board[i]) + j:
                    return False
        return True

    @staticmethod
    def step_cost(state1, action, state2):
        return 1

    def print_solution(self, seq):
        state = self.initial_state
        for action in seq:
            state = self.result(state, action)
            print(state)


class SBPSubproblem(SBPProblem):
    def __init__(self, initial_state, subset):
        super().__init__(initial_state)
        self.subset = subset

    def goal_test(self, state):
        for cell in self.subset:
            i = cell // len(state.board[0])
            j = cell % len(state.board)
            if state.board[i][j] != i * len(state.board[i]) + j:
                return False
        return True

    def step_cost(self, state1, action, state2):
        i, j = state1.find_blank()
        if state2.board[i][j] in self.subset:
            return 1
        return 0

    def result(self, state_, action):
        assert action in SBPSubproblem.actions(state_)
        result_state = state.SBPSubstate(state_.n, self.subset, state_.board)
        di, dj = SBPProblem.moves[action]
        i, j = state_.find_blank()
        result_state.board[i][j], result_state.board[i + di][j + dj] = state_.board[i + di][j + dj], state_.board[i][j]
        return result_state
