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


class Sudoku:

    def __init__(self, difficulty=None):
        self.difficulty = difficulty
        # initialize board based on difficulty/mode
        # accepts board model from grid class

        self.board_model = [
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

        self.copy_board = []
        # self.get_diff()
        # self.board_model = [
        #     [1, 2, 3, 4, 5, 6, 7, 8, 9],
        #     [1, 2, 3, 4, 5, 6, 7, 8, 9],
        #     [1, 2, 3, 4, 5, 6, 7, 8, 9],
        #     [1, 2, 3, 4, 5, 6, 7, 8, 9],
        #     [1, 2, 3, 4, 5, 6, 7, 8, 9],
        #     [1, 2, 3, 4, 5, 6, 7, 8, 9],
        #     [1, 2, 3, 4, 5, 6, 7, 8, 9],
        #     [1, 2, 3, 4, 5, 6, 7, 8, 9],
        #     [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # ]

    def get_board_diff(self):

        if self.difficulty == 'Easy':
            print('generating easy board')
        if self.difficulty == 'Medium':
            print('generating medium board')
        if self.difficulty == 'Hard':
            print('generating hard board')
        if self.difficulty == 'Solving':
            print('Generating empty board')
            self.board_model = self.reset_board(self.board_model)
        elif self.difficulty == '':

            print('Difficulty not set')

    def solve_board(self, mod):

        find = self.find_empty(mod)
        # board is full if no empty spots are found
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.check_valid(mod, i, (row, col)):

                mod[row][col] = i
                # recursively checks the current board by calling solve_board until check valid returns false
                # then steps back the the previous iteration
                if self.solve_board(mod):
                    return True
                # resets the empty spot so it can be tried again
                mod[row][col] = 0

        return False

    def check_valid(self, mod, num, pos):

        # check row
        for i in range(len(mod[0])):
            # check every element in the given row(pos[0]) except the current element (pos[1])
            if mod[pos[0]][i] == num and pos[1] != i:
                return False

        # check column
        for i in range(len(mod[0])):
            # check every element in the given column(pos[1]) except the current element (pos[0])
            if mod[i][pos[1]] == num and pos[0] != i:
                return False

        box_x = pos[1] // 3
        box_y = pos[0] // 3

        # loop only through the elements within the determined box
        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                # check every element in the given box except the element at i,j
                if mod[i][j] == num and (i, j) != pos:
                    return False

        return True

    def print_board(self, mod):

        for i in range(len(mod)):
            # prints horizontal line after 3rd and 6th row
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - - - ")
            for j in range(len(mod[0])):
                # prints veritcal bar after every 3rd and 6th element in each row
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")
                # last element in each row
                if j == 8:
                    print(mod[i][j])
                # every other element, emtpy char instead of newline to keep everything on one line
                else:
                    print(str(mod[i][j]) + " ", end="")

    def find_empty(self, mod):
        for i in range(len(mod)):
            for j in range(len(mod[0])):
                if mod[i][j] == 0:
                    return (i, j)
        return None

    def fill_3x3_box(self, mod, lo, hi):
        l = list(range(1, 10))
        for row in range(lo, hi):
            for col in range(lo, hi):
                num = random.choice(l)
                mod[row][col] = num
                l.remove(num)

    def gen_random_seed(self, mod):
        for i in range(9):
            if i % 3 == 0:
                self.fill_3x3_box(mod, i, i+3)

    # similar to solve except random numbers are tried instead of iterating 1-9
    def gen_full_board(self, mod):
        for row in range(len(mod)):
            for col in range(len(mod[row])):
                if mod[row][col] == 0:
                    num = random.randint(1, 9)

                    if self.check_valid(mod, num, (row, col)):
                        mod[row][col] = num

                    if self.solve_board(mod):
                        self.gen_full_board

                    mod[row][col] = 0

        return False
    # same as solve board but takes a starting position

    def solve_at_pos(self, mod, row, col):
        for n in range(1, 10):
            if self.check_valid(mod, n, (row, col)):
                mod[row][col] = n

                if self.solve_board(mod):
                    return mod

                mod[row][col] = 0

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

    def find_num_solutions(self, mod):
        x = 0
        solutions = []
        for row in range(len(mod)):
            for col in range(len(mod[row])):
                if mod[row][col] == 0:
                    x += 1
        for i in range(1, x+1):

            self.copy_board = mod

            row, col = self.find_Nth_empty(self.copy_board, i)
            copy_sol = self.solve_at_pos(self.copy_board, row, col)
            solutions.append(copy_sol)

        return list(set(solutions))

    def reset_board(self, mod):
        mod = [[0 for j in range(9)] for i in range(9)]
        return mod

# test functionality


def main():

    b = Sudoku()
    my_board = b.board_model
    # my_board = b.reset_board(my_board)
    # b.gen_random_seed(my_board)
    # b.gen_full_board(my_board)
    # b.print_board(my_board)

    sols = b.find_num_solutions(my_board)
    print(sols)


main()
