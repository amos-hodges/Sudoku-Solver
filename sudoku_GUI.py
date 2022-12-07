#################
# Soduko Solver #
#################

## Amos Hodges ##

# GUI created using validate and solve functions

import pygame
from sudoku_solver import check_valid, solve_board, print_board
import time
pygame.font.init()

# End goal:

# A menu interface that:
# 1. allows the user to choose between playing sudoku and entering a puzzle to solve
# 2. allows the player to enter their username to keep track of scores/stats
# 3. if playing sudoku, the user can choose from easy, medium or hard and it will randomly generate
#      -until the window is closed, the program will keep track of how many puzzles are solves, the difficulty and the time for each
#      -when the user is done the program will display the stats and highlight the best game
# 4. if solving sudoku the user can enter numbers on a blank board
#      -the display will indicate which row, column or box if an entry has a conflict
#      -the user can then choose to solve the puzzle one number at a time or all at once
#      -if solving all at once there will be an animation of the back-tracking alogorithm used


class Grid:

    # default board
    board = [
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

    # next step: write method to randomly generate solvable states
    # allow user to enter a board manually to solve, or select from ease, medium, hard

    def __init__(self, rows, cols, width, height):

        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        # initialize squares
        self.squares = [[Square(self.board[i][j], i, j, width, height)
                         for j in range(cols)] for i in range(rows)]
        # to store and update array representation of the board in order to use check_valid and solve_board
        self.model = None
        # to store the coordinates of the currently selected square
        self.selected = None

    def update_model(self):
        self.model = [[self.squares[i][j].value for j in range(
            self.cols)] for i in range(self.rows)]

    # Eventually: instead of checking if the current move is in the solved solution,
    # keep track of user moves with a slightly different color and allow them to go back and change the value
    # write a "hint" functionality using the solve_board function

    def place(self, val):
        # if a square is empty, use the selected position to update the value
        # check if the move is valid and if it is in the correct solved solution
        row, col = self.selected
        if self.squares[row][col].value == 0:
            self.squares[row][col].set(val)
            self.update_model()

            if check_valid(self.model, val, (row, col)) and solve_board(self.model):
                return True

            else:
                self.squares[row][col].set(0)
                self.squares[row][col].set_temp(0)
                self.update_model()
                return False

    def temp_guess(self, val):
        row, col = self.selected
        self.squares[row][col].set_temp(val)

    def select(self, row, col):
        # reset any previously selected squares
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].selected = False

        self.squares[row][col].selected = True
        self.selected = (row, col)

    # used for delete key to remove an entry

    def clear(self):

        row, col = self.selected
        if self.squares[row][col].value == 0:
            self.squares[row][col].set_temp(0)

    def click(self, pos):
        # pygame.mouse.get_pos() returns coordinates relative to the top left corner of the display
        # pos[0] = x_coord, pos[1] = y_coord

        # only return a value when click is within the game display
        if pos[0] < self.width and pos[1] < self.height:
            # divide the board into squares
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(x), int(y))
        else:
            return None

    def is_finished(self):
        # check if there are any empty spaces (0's) left on the board
        for i in range(self.rows):
            for j in range(self.cols):
                if self.squares[i][j].value == 0:
                    return False
        return True

    def draw(self, win):

        # variable to adjust for different size board
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thickness = 4
            else:
                thickness = 1
            # Draw black vertical lines on the window, every 3rd 4x thicker
            pygame.draw.line(win, (0, 0, 0), (0, i*gap),
                             (self.width, i*gap), thickness)
            pygame.draw.line(win, (0, 0, 0), (i*gap, 0),
                             (i*gap, self.height), thickness)

            # draw squares
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].draw(win)


class Square:

    def __init__(self, value, row, col, width, height):

        self.value = value
        # place holder for penciling in guess
        self.temp = 0
        self.row = row
        self.col = col
        # inherit width and height so that squares are scaled to the size of the board
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):

        val_font = pygame.font.SysFont("timesnewroman", 45)
        temp_font = pygame.font.SysFont("timesnewroman", 20)

        gap = self.width / 9
        x = self.row * gap
        y = self.col * gap

        if self.temp != 0 and self.value == 0:
            txt = temp_font.render(str(self.temp), 1, (128, 128, 128))
            # pencil in guess in top left corner of square
            win.blit(txt, (x+5, y+5))

        elif not (self.value == 0):
            txt = val_font.render(str(self.value), 1, (0, 0, 0))
            # render the value in the center of the square
            win.blit(txt, (x + (gap/2 - txt.get_width()/2),
                     y + (gap/2 - txt.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def draw_window(win, board):
    win.fill((255, 255, 255))
    board.draw(win)


def main():

    # change height to accomodate options menu
    window = pygame.display.set_mode((540, 540))
    pygame.display.set_caption("Sudoku Solver")
    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    start = time.time()

    while run:

        play_time = round(time.time()-start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.squares[i][j].temp != 0:
                        if board.place(board.squares[i][j].temp):
                            print('Correct move')
                        else:
                            print('Not correct')
                        key = None

                        if board.is_finished():
                            run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.temp_guess(key)

        draw_window(window, board)

        #redraw_window(window, board)

        pygame.display.update()
    print('Play time: ' + str(play_time) + ' seconds')


main()
pygame.quit()