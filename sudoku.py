#################
# Soduko Solver #
#################

## Amos Hodges ##


## Sudoku class ##
# -impements the rules of sudoku
# -methods to create boards of varying difficulty
# -methods to solve puzzles and check validity of moves

### TO DO: ###
# -make sure the board in Sudoku() object is in sync with the current Game() object
# -finish functions necessary to generate random boards depending on difficulty
# -create helper functions for error indicatation
# -create function for backtracking animation

import random
import copy
from time import time


class Sudoku:

    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.empty_squares = 0
        self.current_move = []
        self.reset_board()
        self.populate_board()
        self.copy_board = []
        self.default = [
            [7, 8, 0, 4, 0, 0, 1, 2, 0],
            [6, 0, 0, 0, 7, 5, 0, 0, 9],
            [0, 0, 0, 6, 0, 1, 0, 7, 8],
            [0, 0, 7, 0, 4, 0, 2, 6, 0],
            [0, 0, 1, 0, 5, 0, 9, 3, 0],
            [9, 0, 4, 0, 6, 0, 0, 0, 5],
            [0, 7, 0, 3, 0, 0, 0, 1, 2],
            [1, 2, 0, 0, 0, 7, 4, 0, 0],
            [0, 4, 9, 2, 0, 6, 0, 0, 7]
        ]

    # testing

    def performance(method):
        def perf_wrapper(*args, **kwargs):
            t1 = time()
            method(*args, **kwargs)
            t2 = time()
            print(f'{method.__name__!r} executed in {(t2-t1):.4f}s')
        return perf_wrapper

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
                #print(f'Current: ({row},{col}) {i}')
                self.current_move.append(((row, col), i))
                if self.solve_board():
                    return True
                # resets the empty spot so it can be tried again
                self.board[row][col] = 0
                self.current_move.append(((row, col), 0))
            else:
                print(f'({row},{col}) {i}')
        return False

    def get_solve_order(self):

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

    def print_board(self):

        for i in range(len(self.board)):
            # prints horizontal line after 3rd and 6th row
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - - - ")
            for j in range(len(self.board[0])):
                # prints veritcal bar after every 3rd and 6th element in each row
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")
                # last element in each row
                if j == 8:
                    print(self.board[i][j])
                # every other element, emtpy char instead of newline to keep everything on one line
                else:
                    print(str(self.board[i][j]) + " ", end="")

    def find_empty(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def fill_3x3_box(self, lo, hi):
        l = list(range(1, 10))
        for row in range(lo, hi):
            for col in range(lo, hi):
                num = random.choice(l)
                self.board[row][col] = num
                l.remove(num)

    def gen_random_seed(self):
        for i in range(9):
            if i % 3 == 0:
                self.fill_3x3_box(i, i+3)

    # similar to solve except random numbers are tried instead of iterating 1-9

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

    def tuple_to_list(self, li):
        return list(list(sub for sub in li))

    def return_solutions(self, li):
        for l in li:
            l = self.tuple_to_list(l)
            # comment out
            self.print_board(l)

    def remove_nums(self, row_col_lo, row_col_hi):
        row = random.randint(row_col_lo, row_col_hi)
        col = random.randint(row_col_lo, row_col_hi)
        if self.board[row][col] != 0:
            self.board[row][col] = 0

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

        # return filled_board
    @performance
    def populate_board(self):
        self.gen_random_seed()
        self.gen_full_board()
        print(f'Populating {self.difficulty} board')
        self.generate_board()

    def reset_board(self):
        self.board = [[0 for j in range(9)] for i in range(9)]
    # to update sudoku board attribute based on new entries to grid

    def update(self, board_rep):
        self.board = board_rep


# test functionality


# def main():

#     b = Sudoku('Easy')

#     # b.get_solve_order()
#     print(b.current_move)


# main()
