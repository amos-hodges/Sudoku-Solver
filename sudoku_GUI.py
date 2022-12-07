#################
# Soduko Solver #
#################

## Amos Hodges ##

# GUI created using validate and solve functions

import pygame
from sudoku_solver import check_valid, solve_board
import time
pygame.init()

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


class Game():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sudoku Solver")

        # state of program
        self.running = True
        # state of game (solver or play)

        # game colors
        self.black, self.white, self.grey, self.dark_grey = (
            0, 0, 0), (255, 255, 255), (128, 128, 128), (80, 80, 80)
        self.playing = False
        self.key = None
        self.display_width = 540
        self.display_height = 600
        self.board = Grid(9, 9, self.display_width, self.display_height)
        self.display = pygame.Surface(
            (self.display_width, self.display_height))
        self.window = pygame.display.set_mode(
            (self.display_width, self.display_height))

        self.MainMenu = Menu(self)

    def game_loop(self):
        while self.running:
            self.check_events()
            self.draw_window()
            pygame.display.update()

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
                clicked = self.board.click(pos)
                if clicked:
                    self.board.select(clicked[0], clicked[1])
                    self.key = None

        if self.board.selected and self.key != None:
            self.board.temp_guess(self.key)

    def draw_window(self):
        self.window.fill(self.white)
        self.board.draw(self.window)

# TO DO:
# create a working menu class
# then create seperate classes for each menu and modify to inherit the parent menu class


class Menu():

    def __init__(self, game):
        self.game = game
        self.middle_w = self.game.display_width / 2
        self.middle_h = self.game.display_height / 2
        self.button_width = 300
        self.button_height = 50
        self.center_w = self.middle_w - (self.button_width/2)
        self.title_font = pygame.font.SysFont('Corbel', 80)
        self.reg_font = pygame.font.SysFont('Corbel', 20)
        self.small_font = pygame.font.SysFont('Corbel', 30)
        self.click = False
        self.button_1 = None
        self.button_2 = None
        self.run_display = True

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        text_width = textobj.get_width()
        textrect = textobj.get_rect()
        textrect.topleft = (x - (text_width/2), y)
        surface.blit(textobj, textrect)

    def create_buttons(self):
        self.button_1 = pygame.Rect(
            self.center_w, 200, self.button_width, self.button_height)
        self.button_2 = pygame.Rect(
            self.center_w, 300, self.button_width, self.button_height)
        pygame.draw.rect(self.game.window, self.game.dark_grey, self.button_1)
        pygame.draw.rect(self.game.window, self.game.dark_grey, self.button_2)

    def get_click(self):

        mx, my = pygame.mouse.get_pos()
        if self.button_1.collidepoint((mx, my)):
            if self.click:
                print('Working: click to game')
                self.run_display = False
        if self.button_2.collidepoint((mx, my)):
            if self.click:
                print('Working: click to solver')
                self.run_display = False
        self.click = False

    def check_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

    def main_menu(self):
        while self.run_display:
            # while self.game.running:
            self.game.window.fill(self.game.grey)

            self.draw_text('Sudoku Solver', self.title_font, self.game.white,
                           self.game.window, self.middle_w, 20)
            self.draw_text('by Amos Hodges', self.reg_font, self.game.white,
                           self.game.window, self.middle_w, 100)
            self.create_buttons()
            self.draw_text('Play Sudoku', self.small_font, self.game.white,
                           self.game.window, self.middle_w, 200+(self.button_height/2)-15)
            self.draw_text('Solve a puzzle for me', self.small_font, self.game.white,
                           self.game.window, self.middle_w, 300+(self.button_height/2)-15)
            self.get_click()
            self.check_events()
            pygame.display.update()


def main():

    solver = Game()
    while solver.running:
        solver.MainMenu.main_menu()
        solver.game_loop()


main()
pygame.quit()
