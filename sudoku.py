#################
# Soduko Solver #
#################

## Amos Hodges ##


## Sudoku class ##
# -impements the rules of sudoku
# -methods to create boards of varying difficulty
# -methods to solve puzzles and check validity of moves

import random


class Sudoku:

    def __init__(self, difficulty=None):
        self.difficulty = difficulty
        # initialize empty board
        self.reset_board()

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

    def reset_board(self):
        self.board = [[0 for j in range(9)] for i in range(9)]
        return self.board

# test functionality


# def main():

#     b = Sudoku()
#     b.print_board()
#     b.gen_random_seed()
#     b.solve_board()
#     b.print_board()


# main()
