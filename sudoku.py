#################
# Soduko Solver #
#################

## Amos Hodges ##


## Sudoku class ##
# -impements the rules of sudoku
# -methods to solve puzzles and check validity of moves
# -methods to create boards of varying difficulty

### TO DO ###
# -remove unused variables
# attmept to speed up board generation
# make sure that each function is absolutely necessary (solve_board,check_valid)
# look for ways to consilidate similar function

import random
import copy
from time import time


class Sudoku:

    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.empty_squares = 0
        # list that is populated by every move attempted during backtracking
        self.current_move = []
        # ordered list of correct moves according to backtracking solve
        self.solution_moves = []
        self.reset_board()
        self.populate_board()
        self.copy_board = []

    # for testing execution times

    def performance(method):
        def perf_wrapper(*args, **kwargs):
            t1 = time()
            method(*args, **kwargs)
            t2 = time()
            print(f'{method.__name__!r} executed in {(t2-t1):.4f}s')
        return perf_wrapper

    # visual for testing functions without GUI

    def print_board(self):
        for i in range(len(self.board)):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - - - ")
            for j in range(len(self.board[0])):

                if j % 3 == 0 and j != 0:
                    print(" | ", end="")
                if j == 8:
                    print(self.board[i][j])
                else:
                    print(str(self.board[i][j]) + " ", end="")

    # set the number of squares to remove

    def get_board_diff(self):

        if self.difficulty == 'Easy':
            self.empty_squares = 32
        if self.difficulty == 'Medium':
            self.empty_squares = 42
        if self.difficulty == 'Hard':
            self.empty_squares = 50
        if self.difficulty == 'Solving':
            self.empty_squares = 0
            self.reset_board()
        elif self.difficulty == '':
            print('Error: difficulty not set')

    # recursively solve a given board using backtracking

    def solve_board(self):

        find = self.find_empty()
        # board is full if no empty spots are found
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):

            if self.check_valid(i, (row, col)):

                self.board[row][col] = i
                # recursively checks the current board by calling solve_board until check valid returns false
                # then steps back the the previous iteration

                if self.solve_board():
                    return True
                # resets the empty spot so it can be tried again
                self.board[row][col] = 0
        return False

    # same as solve board function, used populate the solve order list (solution_moves).

    def get_solve_order(self):

        find = self.find_empty()

        if not find:

            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.check_valid(i, (row, col)):

                self.board[row][col] = i
                self.current_move.append(((row, col), i))
                # recursively checks the current board by calling solve_board until check valid returns false
                # then steps back the the previous iteration
                if self.get_solve_order():
                    self.solution_moves.append(((row, col), i))
                    return True

                self.board[row][col] = 0
                self.current_move.append(((row, col), 0))
        return False

    # check row, col, box for same number

    def check_valid(self, num, pos):

        # check row
        for i in range(len(self.board[0])):
            # check every element in the given row(pos[0]) except the current element (pos[1])
            if self.board[pos[0]][i] == num and pos[1] != i:

                return False

        # check column
        for i in range(len(self.board[0])):
            # check every element in the given column(pos[1]) except the current element (pos[0])
            if self.board[i][pos[1]] == num and pos[0] != i:

                return False

        box_x = pos[1] // 3
        box_y = pos[0] // 3

        # loop only through the elements within the determined box
        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                # check every element in the given box except the element at i,j
                if self.board[i][j] == num and (i, j) != pos:

                    return False

        return True

    # same as check_valid to return collision type and coordinate

    def get_collision(self, num, pos):

        # check row
        for i in range(len(self.board[0])):
            # check every element in the given row(pos[0]) except the current element (pos[1])
            if self.board[pos[0]][i] == num and pos[1] != i:

                return ['row', (pos[0], i)]

        # check column
        for i in range(len(self.board[0])):
            # check every element in the given column(pos[1]) except the current element (pos[0])
            if self.board[i][pos[1]] == num and pos[0] != i:

                return ['column', (i, pos[1])]

        box_x = pos[1] // 3
        box_y = pos[0] // 3

        # loop only through the elements within the determined box
        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                # check every element in the given box except the element at i,j
                if self.board[i][j] == num and (i, j) != pos:

                    return ['box', (i, j)]

        # finally check if the move is in the solution
        if ((pos), num) not in self.solution_moves:
            return ['invalid', (pos[0], pos[1])]
        return True

    # return next empty cell

    def find_empty(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    # iterates through each cell in a 3x3 box, populating with random numbers

    def fill_3x3_box(self, lo, hi):
        l = list(range(1, 10))
        for row in range(lo, hi):
            for col in range(lo, hi):
                num = random.choice(l)
                self.board[row][col] = num
                l.remove(num)

    # fils the 3x3 boxes on the diagonal for the seed of completed board

    def gen_random_seed(self):
        for i in range(9):
            if i % 3 == 0:
                self.fill_3x3_box(i, i+3)

    # popluates the rest of the seed board by filling in random numbers that are valid and are part of the solution

    def gen_full_board(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 0:
                    num = random.randint(1, 9)

                    if self.check_valid(num, (row, col)):
                        self.board[row][col] = num

                    if self.solve_board():
                        self.gen_full_board()

                    self.board[row][col] = 0

        return False

    # same as solve board but takes a starting position

    def solve_at_pos(self, row, col):
        for n in range(1, 10):
            if self.check_valid(n, (row, col)):
                self.board[row][col] = n

                if self.solve_board():
                    return self.board

                self.board[row][col] = 0

        return False

    # same as find empty but returns the empty cell specified by n

    def find_Nth_empty(self, mod, n):
        i = 1
        for row in range(len(mod)):
            for col in range(len(mod[row])):
                if mod[row][col] == 0:
                    if i == n:
                        return (row, col)
                    i += 1
        return False

    # uses find_nth_empty() and solve_at_pos() to solve from every empty spot on the board
    # generates a list of all different solutions

    def find_num_solutions(self):
        x = 0
        solutions = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 0:
                    x += 1
        for i in range(1, x+1):

            copy_board = copy.deepcopy(self)

            row, col = self.find_Nth_empty(copy_board.board, i)

            copy_sol = copy_board.solve_at_pos(row, col)

            copy_sol = tuple(tuple(sub) for sub in copy_sol)
            solutions.append(copy_sol)

        return set(solutions)

    # remove  a number at a randow row/col

    def remove_nums(self, row_col_lo, row_col_hi):
        row = random.randint(row_col_lo, row_col_hi)
        col = random.randint(row_col_lo, row_col_hi)
        if self.board[row][col] != 0:
            self.board[row][col] = 0

    # depending on difficulty, removes a certain number of squares from the full board
    # after 12 are removed, checks that there is a unique solution for each subsequent removed square

    def generate_board(self):

        self.get_board_diff()

        c = 0
        while c < 4:
            self.remove_nums(0, 2)
            c += 1
        c = 0
        while c < 4:
            self.remove_nums(3, 5)
            c += 1
        c = 0
        while c < 4:
            self.remove_nums(6, 8)
            c += 1
        self.empty_squares -= 12
        c = 0
        while c < self.empty_squares:
            row = random.randint(0, 8)
            col = random.randint(0, 8)

            if self.board[row][col] != 0:
                cur_num = self.board[row][col]
                self.board[row][col] = 0

                if len(self.find_num_solutions()) != 1:
                    self.board[row][col] = cur_num
                    continue
                c += 1

    # generates the completed board and then calls generate_board() to remove squares
    # @performance
    def populate_board(self):
        self.gen_random_seed()
        self.gen_full_board()
        self.generate_board()

    def reset_board(self):
        self.board = [[0 for j in range(9)] for i in range(9)]

    # keep sudoku class board in sync with grid/game board

    def update(self, board_rep):
        self.board = board_rep

    def copy_and_solve(self):
        self.copy_board = copy.deepcopy(self.board)
        solvable = self.solve_board()
        self.board = self.copy_board
        return solvable
