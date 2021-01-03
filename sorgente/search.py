from node import Node
from custom_queue import PriorityQueue


def child_node(problem, parent, action):
    state = problem.result(parent.state, action)
    return Node(state,
                parent,
                action,
                parent.path_cost + problem.step_cost(parent.state, action, state))


def astar_search(problem, h, database):
    def get_priority(node_):
        return node_.path_cost + h(node_.state)

    def add_entry(node, database, n):
        database[repr(node.state)] = n
        if node.parent is not None:
            add_entry(node.parent, database, n + problem.step_cost(node.parent.state, node.parent.action, node.state))

    node = Node(problem.initial_state)
    frontier = PriorityQueue()
    frontier.insert(node, get_priority(node))
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            add_entry(node, database, 0)
            return
        elif repr(node.state) in database:
            add_entry(node, database, database[repr(node.state)])
            return
        explored.add(repr(node.state))
        for action in problem.actions(node.state):
            child = child_node(problem, node, action)
            if repr(child.state) not in explored:
                frontier.insert(child, get_priority(child))
    raise FailureError("Goal unreachable")


def f_limited_astar_search(problem, h, limit):
    def recursive_fls_astar(node):
        f = node.path_cost + h(node.state)
        if problem.goal_test(node.state):
            # return node.solution()
            return 1
        elif f > limit:
            raise CutoffError(f, 1, "")
        else:
            cutoff_occurred = False
            next_limit = None
            num_nodes = 1
            for action in problem.actions(node.state):
                child = child_node(problem, node, action)
                try:
                    # return recursive_fls_astar(child)
                    return recursive_fls_astar(child) + num_nodes
                except CutoffError as cutoff_error:
                    cutoff_occurred = True
                    if next_limit is None:
                        next_limit = cutoff_error.next_limit
                    else:
                        next_limit = min(next_limit, cutoff_error.next_limit)
                    num_nodes += cutoff_error.num_nodes
            if cutoff_occurred:
                raise CutoffError(next_limit, num_nodes, "")
            else:
                raise FailureError("Goal unreachable")

    return recursive_fls_astar(Node(problem.initial_state))


def iterative_deepening_astar(problem, h):
    limit = 0
    num_nodes = 0
    while True:
        try:
            return f_limited_astar_search(problem, h, limit) + num_nodes
        except CutoffError as cutoff_error:
            limit = cutoff_error.next_limit
            num_nodes += cutoff_error.num_nodes


class Error(Exception):
    pass


class FailureError(Error):
    def __init__(self, message):
        self.message = message


class CutoffError(Error):
    def __init__(self, next_limit, num_nodes, message):
        self.next_limit = next_limit
        self.num_nodes = num_nodes
        self.message = message
