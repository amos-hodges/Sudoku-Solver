#################
# Soduko Solver #
#################

## Amos Hodges ##

# functions for validating a given entry and solving the board

import random
# test board
# each list represents horizontal row
# 0 represents empty space
sample_board = [
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

empty_board = [[0 for j in range(9)] for i in range(9)]

# populates the 3x3 boxes randomly


def fill_3x3_box(board, lo, hi):
    l = list(range(1, 10))
    for row in range(lo, hi):
        for col in range(lo, hi):
            num = random.choice(l)
            board[row][col] = num
            l.remove(num)


def gen_random_seed(board):
    for i in range(9):
        if i % 3 == 0:
            fill_3x3_box(board, i, i+3)

    ### solve function ###
    # uses find funtion to seek the next empty space
    # iterates 1-9 at the empty space and goes with the first valid option
    # recursively calls itself progressing through the board
    # when an option is invalid, it resets the spot to 0 (empty) and backtracks to the previous correct position


def solve_board(board):

    find = find_empty(board)
    # board is full if no empty spots are found
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if check_valid(board, i, (row, col)):

            board[row][col] = i
            # recursively checks the current board by calling solve_board until check valid returns false
            # then steps back the the previous iteration
            if solve_board(board):
                return True
            # resets the empty spot so it can be tried again
            board[row][col] = 0

    return False


### check if valid entry ###
# check if the number entered at the given position is valid on the current board


def check_valid(board, num, pos):

    # check row
    for i in range(len(board[0])):
        # check every element in the given row(pos[0]) except the current element (pos[1])
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # check column
    for i in range(len(board[0])):
        # check every element in the given column(pos[1]) except the current element (pos[0])
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # check 3x3 box
    # determine which box the given position is in

    #        |        |
    #  0,0   |  0,1   |  0,2
    #        |        |
    # - - - - - - - - - - - - -
    #        |        |
    #  1,0   |  1,1   |  1,2
    #        |        |
    # - - - - - - - - - - - - -
    #        |        |
    #  2,0   |  2,1   |  2,2
    #        |        |

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    # loop only through the elements within the determined box
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            # check every element in the given box except the element at i,j
            if board[i][j] == num and (i, j) != pos:
                return False

    return True

### display the arrray as sudoku board ###
# print board array in and orgnaized grid for testing functionality #


def print_board(board):

    for i in range(len(board)):
        # prints horizontal line after 3rd and 6th row
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")
        for j in range(len(board[0])):
            # prints veritcal bar after every 3rd and 6th element in each row
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            # last element in each row
            if j == 8:
                print(board[i][j])
            # every other element, emtpy char instead of newline to keep everything on one line
            else:
                print(str(board[i][j]) + " ", end="")


### find next empty space ###
# iterates over current board and returns the position of the next available empty space

def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None


# test functionality of solve
# print_board(sample_board)
# solve_board(sample_board)
# print("-----------------------------")
# print_board(sample_board)
print_board(empty_board)
gen_random_seed(empty_board)
print_board(empty_board)
solve_board(empty_board)
print_board(empty_board)
