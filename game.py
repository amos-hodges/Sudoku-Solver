#################
# Soduko Solver #
#################

## Amos Hodges ##

# End goal:

# [X]   1. allows the user to choose between playing sudoku and entering a puzzle to solve
# [X]   2. allows the player to enter their username
# [X]   3. if playing sudoku, the user can choose from easy, medium or hard and it will randomly generate
# [X]    -until the window is closed, the program will keep track of how many puzzles are solves, the difficulty and the time for each
# [X]    -when the user is done the program will display the stats and highlight the best game
# [X]   4. if solving sudoku the user can enter numbers on a blank board
# [X]    -a toggle before each game if the user would like to use the collision/ wrong move guides
# [X]    -the display will indicate which row, column or box if an entry has a conflict
# [X]    -the user can then choose to solve the puzzle one number at a time or all at once
# [X]    -if solving all at once there will be an animation of the back-tracking alogorithm used
# [X]   5. a 'play again/solve more' page upon completing a puzzle in either mode


# 1/9/23 CURRENT TASK:

# game functions like it is supposed to
# -need to remove appended moves from solution_moves if it is undone
# -temp vals are increasing move num
# -issue with solve mode get_solver_order threshold.
#  Need to make sure the minimum number of enties is guaranteed to be 17+
# - figure out why squares that have been 'undone' show up blank after the board has been solved
# -if guide mode is off, wrong guesses need to be black
#
#
# -work out existing bugs/edgecases and coninue to diagnose
# -optimize board generation
# -clean each file, make sure placement of methods make sense
# maybe:
# simple data base that stores games for unique usernames, possible to retreive best games


### CURRENT BUGS/ISSUES ###

#
# -the current is_finished only checks that the board is full,
# so there will need to ba a check that the full board matches the solved board
#
# -hard board can take a long time to generate, think about how to optimize
# -font may not be available on all machines, figure out how to make sure there is a default that looks good.


import pygame
from sudoku import *
from menu import *
import time

import random


class Grid:

    def __init__(self, rows, cols, width, height, difficulty):

        self.rows = rows
        self.cols = cols

        self.game_play = Sudoku(difficulty)
        self.board = self.game_play.board

        # initialize squares
        self.squares = [[Square(self.board[i][j], i, j, width, height)
                         for j in range(cols)] for i in range(rows)]
        # variable to hold collision info, might not need
        self.collision = None
        self.width = width
        self.height = height
        # to store the coordinates of the currently selected square
        self.selected = None
        self.solve_idx = 0
        self.hint_num = []
        self.hint_idx = 0
        self.move_list = []
        self.move_num = 0

    # keep grid class board in sync with the display board

    def update_model(self):
        self.board = [[self.squares[i][j].value for j in range(
            self.cols)] for i in range(self.rows)]

    def reset_squares(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].value = 0

    def place(self, val):

        # if a square is empty, use the selected position to update the value
        # check if the move is valid and if it is in the correct solved solution
        row, col = self.selected
        if self.squares[row][col].value == 0:
            self.squares[row][col].set(val)

            self.update_model()
            self.game_play.update(self.board)

            if ((row, col), val) in self.game_play.solution_moves:
                self.squares[row][col].set_wrong(0)
                self.move_list.append((row, col))
                self.move_num += 1
                return True

            else:
                self.squares[row][col].set(0)
                self.squares[row][col].set_temp(0)
                self.squares[row][col].set_wrong(val)

                self.update_model()
                self.game_play.update(self.board)
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
    # deleting temp guess using del key

    def clear(self):

        row, col = self.selected
        if self.squares[row][col].value == 0:
            self.squares[row][col].set_temp(0)
        if self.squares[row][col].wrong != 0:
            self.squares[row][col].set_temp(0)
            self.squares[row][col].set_wrong(0)
        # elif (self.squares[row][col].value != 0) and self.wrong_move

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
    # highlight row/col/box and the number that causes the collision

    def draw_collision(self, win):
        gap = self.width / 9

        if self.collision[0] == 'row':
            pygame.draw.rect(
                win, (255, 0, 0), (0, self.collision[1][0]*gap, gap*9, gap), 1)
            pygame.draw.rect(
                win, (255, 0, 0), (self.collision[1][1]*gap, self.collision[1][0]*gap, gap, gap), 4)
        if self.collision[0] == 'column':
            pygame.draw.rect(
                win, (255, 0, 0), (self.collision[1][1]*gap, 0, gap, gap*9), 1)
            pygame.draw.rect(
                win, (255, 0, 0), (self.collision[1][1]*gap, self.collision[1][0]*gap, gap, gap), 4)
        if self.collision[0] == 'box':
            pygame.draw.rect(
                win, (255, 0, 0), ((self.collision[1][1]//3)*gap*3, (self.collision[1][0]//3)*gap*3, gap*3, gap*3), 1)
            pygame.draw.rect(
                win, (255, 0, 0), (self.collision[1][1]*gap, self.collision[1][0]*gap, gap, gap), 4)
        if self.collision[0] == 'invalid':

            pygame.draw.rect(
                win, (255, 255, 0), (self.collision[1][1]*gap, self.collision[1][0]*gap, gap, gap), 4)

    # gets the row,col & value from the backtracking move list at the current index

    def backtracking_solve(self):

        if self.solve_idx < len(self.game_play.current_move):

            (row, col), val = self.game_play.current_move[self.solve_idx]

            self.squares[row][col].set(val)

            # slow the backtracking proportional to completedness
            #time.sleep(((row+1)**2 * (col+1)**2)/10000)

            self.solve_idx += 1

    def get_sleep_time(self):
        pass

    def insert_hint(self):
        self.hint_idx = random.choice(self.hint_num)
        (row, col), val = self.game_play.solution_moves[self.hint_idx]
        if self.squares[row][col].value == 0:
            self.squares[row][col].set(val)
            self.move_list.append((row, col))
            self.move_num += 1
            return False
        else:
            return True

    def undo_move(self):
        if self.move_num > 0:
            row, col = self.move_list[self.move_num-1]
            self.squares[row][col].value = 0
            self.squares[row][col].set_temp(0)
            self.squares[row][col].set_wrong(0)
            self.move_list.pop(self.move_num-1)
            self.move_num -= 1

    def update_solve_order(self):
        if self.selected:
            row, col = self.selected
            self.game_play.solution_moves.append(
                ((row, col), self.squares[row][col].temp))


class Square:

    def __init__(self, value, row, col, width, height):

        self.value = value
        # place holder for penciling in guess
        self.temp = 0
        # fills in the entry in a different color, can be removed by user
        self.wrong = 0
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

        #######################################################
        elif not (self.wrong == 0) and self.value == 0:
            txt = val_font.render(str(self.wrong), 1, (128, 128, 128))
            # render the value in the center of the square
            win.blit(txt, (x + (gap/2 - txt.get_width()/2),
                     y + (gap/2 - txt.get_height()/2)))
        ######################################################
        elif not (self.value == 0):
            # print('value')
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

    def set_wrong(self, val):
        self.wrong = val


class Game():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sudoku Solver")

        self.running = True
        self.playing = False
        self.mode = 'playing'
        self.difficulty = 'Solving'

        self.black, self.white, self.grey, self.dark_grey = (
            0, 0, 0), (255, 255, 255), (128, 128, 128), (80, 80, 80)
        self.blue = (36, 142, 191)
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
                          self.display_height, self.difficulty)
        self.button_width = (self.display_width/3)-10
        self.button_height = (self.display_height-self.display_width)-10

        self.main_menu = MainMenu(self)
        self.diff_menu = DiffMenu(self)
        self.again_menu = AgainMenu(self)
        self.stats_menu = Stats(self)
        self.curr_menu = self.main_menu
        self.play_options = ['Undo', 'Hint', 'Solve']
        self.solve_options = ['Undo', 'Step', 'Solve']

        self.username = ''
        self.stats = []
        self.curr_game = 0
        self.game_time = 0
        self.hints_used = 0
        self.key = None

        self.guide_mode = False

        self.solve_clicked = False
        self.clash = False

    def game_loop(self):
        # get board soltions before starting game(needed for place() function to work)
        if self.difficulty != 'Solving':
            self.board.game_play.get_solve_order()

        self.clash = False
        start = time.time()
        while self.playing:

            # self.check_events()

            if self.solve_clicked:
                self.board.backtracking_solve()
            else:
                self.check_events()

            self.draw_window()

            if self.clash:
                self.board.draw_collision(self.window)

            pygame.display.update()
            # check after last number is updated
            if self.board.is_finished():
                stop = time.time()
                self.game_time = time.strftime(
                    "%M:%S", time.gmtime(stop-start))
                time.sleep(5)
                self.curr_game += 1
                self.update_stats()
                self.reset_stat_counters()

                self.solve_clicked = False
                self.board.reset_squares()

                #self.curr_menu = self.stats_menu
                self.curr_menu = self.again_menu
                self.curr_menu.run_display = True
                self.playing = False

    # note: should this method be moved to menu.py?
    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        text_width = textobj.get_width()
        textrect = textobj.get_rect()
        textrect.topleft = (x - (text_width/2), y)
        surface.blit(textobj, textrect)

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

                if self.board.selected:
                    if event.key == pygame.K_LEFT:
                        if self.board.selected[1] > 0:
                            self.board.select(
                                self.board.selected[0], self.board.selected[1]-1)
                            self.key = None
                    if event.key == pygame.K_RIGHT:
                        if self.board.selected[1] < 8:
                            self.board.select(
                                self.board.selected[0], self.board.selected[1]+1)
                            self.key = None
                    if event.key == pygame.K_UP:
                        if self.board.selected[0] > 0:
                            self.board.select(
                                self.board.selected[0]-1, self.board.selected[1])
                            self.key = None
                    if event.key == pygame.K_DOWN:
                        if self.board.selected[0] < 8:
                            self.board.select(
                                self.board.selected[0]+1, self.board.selected[1])
                            self.key = None

                if event.key == pygame.K_DELETE:
                    self.board.clear()
                    self.key = None
                    self.board.update_model()
                    self.board.game_play.update(self.board.board)
                if event.key == pygame.K_ESCAPE:
                    self.curr_menu = self.main_menu
                    self.playing = False

                if event.key == pygame.K_RETURN:

                    i, j = self.board.selected
                    if self.board.squares[i][j].temp != 0:

                        # if in solving mode, the first 17 moves populate the solution moves
                        # as long as there are no collisions. after 17 moves, the solve order is calculated
                        # using the existing moves, after which moves that are not in the solution
                        # will show up in yellow. There are likely edge cases that will cause errors

                        if (self.difficulty == 'Solving'):
                            if (self.board.move_num < 17) or len(set(self.board.game_play.solution_moves)) < 17:

                                if ((i, j), self.board.squares[i][j].temp) not in self.board.game_play.solution_moves:

                                    if (self.board.squares[i][j].value) == 0:

                                        self.board.game_play.solution_moves.append(
                                            ((i, j), self.board.squares[i][j].temp))

                                        if (self.board.game_play.get_collision(
                                                self.board.squares[i][j].temp, self.board.selected)) != True:
                                            self.board.game_play.solution_moves.pop()
                                            #self.board.move_num -= 1
                                        self.board.update_model()
                                        self.board.game_play.update(
                                            self.board.board)
                                print('not safe to solve')
                            elif (self.board.move_num >= 17) and len(set(self.board.game_play.solution_moves)) >= 17:
                                print('getting solution')
                                self.board.game_play.get_solve_order()

                        # place the number
                        if self.board.place(self.board.squares[i][j].temp):
                            self.clash = False
                            self.board.collision = ['none', (0, 0)]
                            self.board.update_model()
                            self.board.game_play.update(self.board.board)

                        # check for row/col/box collision, guide mode toggle
                        if self.board.squares[i][j].value == 0 and self.guide_mode:

                            self.board.collision = self.board.game_play.get_collision(
                                self.key, self.board.selected)

                            if self.board.squares[i][j].wrong != 0:
                                self.board.collision = self.board.game_play.get_collision(
                                    self.board.squares[i][j].wrong, self.board.selected)

                            self.board.move_list.append((i, j))
                            self.board.move_num += 1

                        if self.board.collision:
                            self.clash = True

                        self.key = None
                    print(len(self.board.move_list))
                    print(self.board.move_num)
                    print(len(set(self.board.game_play.solution_moves)))
            if event.type == pygame.MOUSEBUTTONDOWN:
                # left click only
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    # click on game board
                    if pos[1] < self.display_width:
                        clicked = self.board.click(pos)
                        self.clash = False
                        if clicked:
                            self.board.select(clicked[0], clicked[1])
                            self.key = None
                    # click on buttons
                    elif self.solve_btn.collidepoint(pos):
                        # prevent solving unless the minimum number is met
                        if (self.difficulty == 'Solving') and (self.board.move_num < 17):
                            pass
                        else:
                            self.board.solve_idx = 0
                            self.board.game_play.get_solve_order()
                            self.solve_clicked = True
                            self.key = None

                    elif self.mid_butn.collidepoint(pos) and not self.solve_clicked:
                        if (self.difficulty == 'Solving') and (self.board.move_num < 17):
                            pass
                        else:
                            # Note: is it possible to call these once instead of every click?
                            self.board.game_play.get_solve_order()
                            self.board.hint_num = [
                                *range(len(self.board.game_play.solution_moves))]
                            while self.board.insert_hint():
                                pass
                            self.hints_used += 1
                    elif self.undo_btn.collidepoint(pos):
                        self.board.undo_move()
                        self.clash = False

        if self.board.selected and self.key != None:

            self.board.temp_guess(self.key)

    def draw_window(self):
        self.window.fill(self.white)
        self.board.draw(self.window)
        self.create_buttons()

    # method to reinitialize board based on difficulty
    # maybe change to 'set_difficulty'
    def get_diff(self):
        self.board = Grid(9, 9, self.display_width,
                          self.display_height, self.difficulty)

    def update_stats(self):
        guided = ''
        solver = ''

        if self.guide_mode:
            guided = 'Yes'
        else:
            guided = 'No'

        if self.solve_clicked:
            solver = 'Yes'
        else:
            solver = 'No'

        self.stats.append([str(self.curr_game), self.difficulty, str(self.game_time),
                           guided, str(self.hints_used), solver])

    def reset_stat_counters(self):
        self.game_time = 0
        self.hints_used = 0


def main():

    solver = Game()

    while solver.running:
        solver.curr_menu.display_menu()
        solver.game_loop()


main()
pygame.quit()
