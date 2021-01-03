import pickle
from time import time

import problem
import search
import heuristic
import state

n = 4
num_tests = 2080

manhattan_time = 0
linear_conflicts_time = 0
disjoint_time = 0
disjoint_reflect_time = 0

manhattan_nodes = 0
linear_conflicts_nodes = 0
disjoint_nodes = 0
disjoint_reflect_nodes = 0

subsets = [set(range(1, (n ** 2 + 1) // 2)), set(range((n ** 2 + 1) // 2, n ** 2))]

databases = []
with open("data1.pickle", "rb") as file:
    databases.append(pickle.load(file))
with open("data2.pickle", "rb") as file:
    databases.append(pickle.load(file))

for i in range(num_tests):
    sbps = state.SBPState(n)
    sbpp = problem.SBPProblem(sbps)
    print("test number", i)
    print(sbps)

    manhattan_time -= time()
    manhattan_nodes += search.iterative_deepening_astar(sbpp, heuristic.manhattan_heuristic)
    manhattan_time += time()

    linear_conflicts_time -= time()
    linear_conflicts_nodes += search.iterative_deepening_astar(sbpp, heuristic.linear_conflicts_heuristic)
    linear_conflicts_time += time()

    disjoint_time -= time()
    disjoint_nodes += search.iterative_deepening_astar(sbpp, lambda
        s: heuristic.disjoint_database_heuristic(s, subsets, databases))
    disjoint_time += time()

    disjoint_reflect_time -= time()
    disjoint_reflect_nodes += search.iterative_deepening_astar(sbpp, lambda
        s: heuristic.disjoint_database_reflection_heuristic(s, subsets, databases))
    disjoint_reflect_time += time()

manhattan_time /= num_tests
linear_conflicts_time /= num_tests
disjoint_time /= num_tests
disjoint_reflect_time /= num_tests

manhattan_nodes /= num_tests
linear_conflicts_nodes /= num_tests
disjoint_nodes /= num_tests
disjoint_reflect_nodes /= num_tests

print("manhattan", manhattan_time, manhattan_nodes)
print("linear conflicts", linear_conflicts_time, linear_conflicts_nodes)
print("disjoint database", disjoint_time, disjoint_nodes)
print("disjoint database with reflections", disjoint_reflect_time, disjoint_reflect_nodes)
