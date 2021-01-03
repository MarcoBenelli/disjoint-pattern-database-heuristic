from copy import deepcopy
from random import shuffle


class State:

    def __eq__(self, other):
        return repr(self) == repr(other)


class SBPState(State):

    def __init__(self, n, board=None):
        self.n = n
        if board is not None:
            self.board = deepcopy(board)
        else:
            linear_board = list(range(n ** 2))
            shuffle(linear_board)
            parity = 0

            # test parity of permutation
            board_copy = list(linear_board)
            i = 0
            while i < len(board_copy):
                if board_copy[i] != i:
                    tmp = board_copy[i]
                    board_copy[i] = board_copy[tmp]
                    board_copy[tmp] = tmp
                    parity += 1
                else:
                    i += 1

            # create 2D board and get manhattan distance of blank tile
            self.board = []
            for i in range(n):
                self.board.append([])
                for j in range(n):
                    cell = linear_board[n * i + j]
                    self.board[i].append(cell)
                    if cell == 0:
                        parity += i + j

            # swaps if odd parity
            if parity % 2 != 0:
                a, b = 0, 1
                if self.board[0][0] == 0:
                    a = 2
                elif self.board[0][1] == 0:
                    b = 2  # assumes n > 2
                self.board[0][a], self.board[0][b] = self.board[0][b], self.board[0][a]

    def __repr__(self):
        string = ""
        for row in self.board:
            for cell in row:
                string += str(cell) + ","
            string += ";"
        return string

    def find_blank(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    return i, j

    def __str__(self):
        string = ""
        for row in self.board:
            for cell in row:
                if cell == 0:
                    string += " "
                else:
                    string += str(cell)
                string += " "
            string += "\n"
        return string


class SBPSubstate(SBPState):

    def __init__(self, n, subset, board=None):
        super().__init__(n, board)
        self.subset = subset

    def __repr__(self):
        string = ""
        for row in self.board:
            for cell in row:
                if cell != 0 and cell not in self.subset:
                    cell = -1
                string += str(cell) + ","
            string += ";"
        return string
