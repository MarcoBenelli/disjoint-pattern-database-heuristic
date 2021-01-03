import pickle
from itertools import permutations
from time import time

import heuristic
import problem
import search
import state


def make_board(permutation, n, offset=0):
    board = [[-1 for j in range(n)] for i in range(n)]
    for k in range(len(permutation)):
        cell = permutation[k]
        if k > 0:
            k += offset
        board[cell // n][cell % n] = k
    return board


n = 4
cell_list = list(range(n ** 2))

dictionary1 = {}
subset1 = set(range(1, (n ** 2 + 1) // 2))
value = -1
starting_time = time()
for permutation in permutations(cell_list, (n ** 2 + 1) // 2):
    if permutation[n ** 2 // 4] != value:
        value = permutation[n ** 2 // 4]
        print("time elapsed: ", int(time() - starting_time))
        print(permutation)
        print("dictionary length: ", len(dictionary1))
    board1 = make_board(permutation, n)
    sbpss1 = state.SBPSubstate(n, subset1, board1)
    sbpsp1 = problem.SBPSubproblem(sbpss1, subset1)
    search.astar_search(sbpsp1, lambda x: heuristic.linear_conflicts_subset_heuristic(x, subset1), dictionary1)
with open('data1.pickle', 'wb') as file:
    pickle.dump(dictionary1, file, pickle.HIGHEST_PROTOCOL)
print("first dictionary completed")

dictionary2 = {}
subset2 = set(range((n ** 2 + 1) // 2, n ** 2))
value = -1
starting_time = time()
for permutation in permutations(cell_list, n ** 2 - (n ** 2 + 1) // 2 + 1):
    if permutation[n ** 2 // 4] != value:
        value = permutation[n ** 2 // 4]
        print("time elapsed: ", int(time() - starting_time))
        print(permutation)
        print("dictionary length: ", len(dictionary2))
    board2 = make_board(permutation, n, (n ** 2 - 1) // 2)
    sbpss2 = state.SBPSubstate(n, subset2, board2)
    sbpsp2 = problem.SBPSubproblem(sbpss2, subset2)
    search.astar_search(sbpsp2, lambda x: heuristic.linear_conflicts_subset_heuristic(x, subset2), dictionary2)
with open('data2.pickle', 'wb') as file:
    pickle.dump(dictionary2, file, pickle.HIGHEST_PROTOCOL)
print("second dictionary completed")
