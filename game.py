#################
# Soduko Solver #
#################

## Amos Hodges ##

# GUI created using validate and solve functions

### TO DO: ###
# -finish creating separate Game() class children for Solve() and Play()
# -check for unused variables and simplify
# -impliment undo, help/step , and solve buttons

import pygame
#from sudoku_solver import check_valid, solve_board, print_board
from sudoku import *
from menu import *
import time
pygame.init()

# End goal:

#   A menu interface that:
# [ ]   1. allows the user to choose between playing sudoku and entering a puzzle to solve
# [ ]   2. allows the player to enter their username to keep track of scores/stats
# [ ]   3. if playing sudoku, the user can choose from easy, medium or hard and it will randomly generate
# [ ]    -until the window is closed, the program will keep track of how many puzzles are solves, the difficulty and the time for each
# [ ]    -when the user is done the program will display the stats and highlight the best game
# [ ]   4. if solving sudoku the user can enter numbers on a blank board
# [ ]    -the display will indicate which row, column or box if an entry has a conflict
# [ ]    -the user can then choose to solve the puzzle one number at a time or all at once
# [ ]    -if solving all at once there will be an animation of the back-tracking alogorithm used
# [ ]   5. a 'play again/solve more' page upon completing a puzzle in either mode


class Grid:

    # default board
    # board = [
    #     [7, 8, 0, 4, 0, 0, 1, 2, 0],
    #     [6, 0, 0, 0, 7, 5, 0, 0, 9],
    #     [0, 0, 0, 6, 0, 1, 0, 7, 8],
    #     [0, 0, 7, 0, 4, 0, 2, 6, 0],
    #     [0, 0, 1, 0, 5, 0, 9, 3, 0],
    #     [9, 0, 4, 0, 6, 0, 0, 0, 5],
    #     [0, 7, 0, 3, 0, 0, 0, 1, 2],
    #     [1, 2, 0, 0, 0, 7, 4, 0, 0],
    #     [0, 4, 9, 2, 0, 6, 0, 0, 7]
    # ]

    # next step: write method to randomly generate solvable states
    # allow user to enter a board manually to solve, or select from ease, medium, hard

    def __init__(self, rows, cols, width, height):

        self.rows = rows
        self.cols = cols

        # conver to function that sets the board based on the game mode
        self.game_play = Sudoku()

        self.board = self.game_play.board_model
        self.model = None

        # initialize squares
        self.squares = [[Square(self.board[i][j], i, j, width, height)
                         for j in range(cols)] for i in range(rows)]

        self.width = width
        self.height = height
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

            if self.game_play.check_valid(self.model, val, (row, col)) and self.game_play.solve_board(self.model):
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
            return (int(y), int(x))
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
                             (i*gap, self.height - gap), thickness)

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
        x = self.col * gap
        y = self.row * gap

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


class Game():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sudoku Solver")

        self.running = True
        self.playing = False
        self.mode = 'playing'

        self.black, self.white, self.grey, self.dark_grey = (
            0, 0, 0), (255, 255, 255), (128, 128, 128), (80, 80, 80)
        self.title_font = pygame.font.SysFont('Corbel', 80)
        self.reg_font = pygame.font.SysFont('Corbel', 20)
        self.small_font = pygame.font.SysFont('Corbel', 30)
        self.misc_font = pygame.font.SysFont(None, 40)

        self.display_width = 540
        self.display_height = 600
        self.display = pygame.Surface(
            (self.display_width, self.display_height))
        self.window = pygame.display.set_mode(
            (self.display_width, self.display_height))
        self.board = Grid(9, 9, self.display_width,
                          self.display_height)
        self.button_width = (self.display_width/3)-10
        self.button_height = (self.display_height-self.display_width)-10

        self.main_menu = MainMenu(self)
        self.diff_menu = DiffMenu(self)
        # self.again_menu
        # self.stats_menu
        self.curr_menu = self.main_menu
        self.play_options = ['Undo', 'Hint', 'Solve']
        self.solve_options = ['Undo', 'Step', 'Solve']

        self.username = 'test'

        self.key = None

    def game_loop(self):
        while self.playing:
            self.check_events()
            self.draw_window()
            pygame.display.update()

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        text_width = textobj.get_width()
        textrect = textobj.get_rect()
        textrect.topleft = (x - (text_width/2), y)
        surface.blit(textobj, textrect)

# MAke genecric function to display text options based on which class is using it
    def create_buttons(self):

        if self.mode == 'playing':
            options = self.play_options
        if self.mode == 'solving':
            options = self.solve_options

        self.undo_btn = pygame.Rect(
            5, self.display_width+6, self.button_width, self.button_height)
        self.mid_butn = pygame.Rect(
            self.button_width+15, self.display_width+6, self.button_width, self.button_height)
        self.solve_btn = pygame.Rect(
            (self.button_width*2)+25, self.display_width+6, self.button_width, self.button_height)

        pygame.draw.rect(self.window, self.grey, self.undo_btn)
        pygame.draw.rect(self.window, self.grey, self.mid_butn)
        pygame.draw.rect(self.window, self.grey, self.solve_btn)
        for i in range(1, 6, 2):

            self.draw_text(options[i//2], self.small_font, self.white,
                           self.window, i*90, self.display_width+15)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.key = 1
                if event.key == pygame.K_2:
                    self.key = 2
                if event.key == pygame.K_3:
                    self.key = 3
                if event.key == pygame.K_4:
                    self.key = 4
                if event.key == pygame.K_5:
                    self.key = 5
                if event.key == pygame.K_6:
                    self.key = 6
                if event.key == pygame.K_7:
                    self.key = 7
                if event.key == pygame.K_8:
                    self.key = 8
                if event.key == pygame.K_9:
                    self.key = 9
                if event.key == pygame.K_DELETE:
                    self.board.clear()
                    self.key = None
                if event.key == pygame.K_ESCAPE:
                    self.curr_menu = self.main_menu
                    self.playing = False
                if event.key == pygame.K_RETURN:
                    i, j = self.board.selected
                    if self.board.squares[i][j].temp != 0:
                        # TO DO:
                        # Impliment an error system for invalid moves (show which row column or square causes the error)
                        # Player entered moves show up in a slightly different color and can be changed
                        # Hint button to show next move in solve_board
                        # undo button to take away last move?
                        if self.board.place(self.board.squares[i][j].temp):
                            print('Correct move')

                        else:
                            print('Not correct')
                        self.key = None

                        if self.board.is_finished():
                            self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # click on game board
                if pos[1] < self.display_width:
                    clicked = self.board.click(pos)
                    if clicked:
                        self.board.select(clicked[0], clicked[1])
                        self.key = None
                # click on button
                else:
                    print('clicking a button')
        if self.board.selected and self.key != None:
            self.board.temp_guess(self.key)

    def draw_window(self):
        self.window.fill(self.white)
        self.board.draw(self.window)
        self.create_buttons()


def main():

    solver = Game()

    while solver.running:
        solver.curr_menu.display_menu()

        # solver.main_menu.display_menu()
        # solver.diff_menu.display_menu()
        solver.game_loop()


main()
pygame.quit()
