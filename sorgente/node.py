class Node:

    def __init__(self, state, parent=None, action=None, path_cost=0, priority=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.priority = priority

    def __eq__(self, other):
        return self.state == other.state

    def __repr__(self):
        return repr(self.state)

    def solution(self):
        if self.parent is None:
            return []
        seq = self.parent.solution()
        seq.append(self.action)
        return seq
