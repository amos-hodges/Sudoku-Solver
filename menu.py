#################
# Soduko Solver #
#################

## Amos Hodges ##

## menu classes #

### TO DO: ###
# -finish menu stats page
# -highlight difficulty selected
# -make sure user name and difficulty are required to start a game
# -consolidate redundant methods to the parent class
# -once game classes are complete make sure selection
#  & escape sequences are correct

import pygame


class Menu():

    def __init__(self, game):
        self.game = game
        self.middle_w = self.game.display_width / 2
        self.middle_h = self.game.display_height / 2
        self.button_width = 300
        self.button_height = 50
        self.center_w = self.middle_w - (self.button_width/2)
        self.click = False
        self.run_display = True
        self.active_color = (200, 200, 200)
        self.passive_color = (150, 150, 150)
        self.curr_color = self.passive_color

        self.click_active = False
        self.choice_active = False

    def check_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.curr_menu = self.game.main_menu
                    self.run_display = False
                    # pygame.quit()

                if self.click_active:

                    if event.key == pygame.K_BACKSPACE:
                        self.game.username = self.game.username[:-1]
                    else:
                        if len(self.game.username) <= 15:
                            if (event.key == pygame.K_RETURN):
                                self.click_active = False
                            else:
                                self.game.username += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                # left click
                if event.button == 1:
                    self.click = True

    def get_color(self):
        if self.click_active:
            self.curr_color = self.active_color

        else:
            self.curr_color = self.passive_color


# Main Menu / Title Page


class MainMenu(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)

    def create_menu(self):

        self.game.window.fill(self.game.grey)

        self.game.draw_text('Sudoku Solver', self.game.title_font, self.game.white,
                            self.game.window, self.middle_w, 20)
        self.game.draw_text('by Amos Hodges', self.game.reg_font, self.game.white,
                            self.game.window, self.middle_w, 100)

        self.play_game_btn = pygame.Rect(
            self.center_w, 200, self.button_width, self.button_height)
        self.solve_puz_btn = pygame.Rect(
            self.center_w, 300, self.button_width, self.button_height)
        pygame.draw.rect(self.game.window,
                         self.game.dark_grey, self.play_game_btn)
        pygame.draw.rect(self.game.window,
                         self.game.dark_grey, self.solve_puz_btn)
        self.game.draw_text('Play Sudoku', self.game.small_font, self.game.white,
                            self.game.window, self.middle_w, 200+(self.button_height/2)-15)
        self.game.draw_text('Solve a puzzle for me', self.game.small_font, self.game.white,
                            self.game.window, self.middle_w, 300+(self.button_height/2)-15)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.create_menu()
            self.get_click()
            self.check_events()
            pygame.display.update()

    def get_click(self):

        mx, my = pygame.mouse.get_pos()

        if self.click:
            if self.play_game_btn.collidepoint((mx, my)):
                self.game.curr_menu = self.game.diff_menu
                self.game.mode = 'playing'
                self.run_display = False
            if self.solve_puz_btn.collidepoint((mx, my)):

                self.game.difficulty = 'Solving'
                self.game.get_diff()
                self.game.playing = True
                self.game.mode = 'solving'
                self.run_display = False
                #self.game.board.game_play.solution_moves = []
        self.click = False


# Enter username / select difficulty


class DiffMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.color1 = self.passive_color
        self.color2 = self.passive_color
        self.color3 = self.passive_color

    def create_menu(self):

        self.game.window.fill(self.game.grey)
        self.game.draw_text('Enter Username:', self.game.small_font, self.game.white,
                            self.game.window, self.middle_w, 100)
        self.game.draw_text('Select difficulty:', self.game.small_font, self.game.white,
                            self.game.window, self.middle_w, 240)
        # username input
        self.usr_input = pygame.Rect(
            self.center_w, 150, self.button_width, self.button_height)
        # difficulty
        self.easy_btn = pygame.Rect(
            self.middle_w-self.button_width/4, 280, self.button_width/2, self.button_height-15)
        self.med_btn = pygame.Rect(
            self.middle_w-self.button_width/4, 320, self.button_width/2, self.button_height-15)
        self.hard_btn = pygame.Rect(
            self.middle_w-self.button_width/4, 360, self.button_width/2, self.button_height-15)
        # play button
        self.play_btn = pygame.Rect(
            self.center_w, 450, self.button_width, self.button_height)

        self.get_color()
        self.set_option_color()

        pygame.draw.rect(self.game.window, self.curr_color, self.usr_input)
        pygame.draw.rect(self.game.window, self.color1, self.easy_btn)
        pygame.draw.rect(self.game.window, self.color2, self.med_btn)
        pygame.draw.rect(self.game.window, self.color3, self.hard_btn)
        pygame.draw.rect(self.game.window, self.game.dark_grey, self.play_btn)

        # username input

        self.game.draw_text(self.game.username, self.game.misc_font, self.game.blue,
                            self.game.window, self.middle_w, 150+(self.button_height/2)-10)
        # difficulty
        self.game.draw_text('Easy', self.game.reg_font, self.game.white,
                            self.game.window, self.middle_w, 287)
        self.game.draw_text('Medium', self.game.reg_font, self.game.white,
                            self.game.window, self.middle_w, 327)
        self.game.draw_text('Hard', self.game.reg_font, self.game.white,
                            self.game.window, self.middle_w, 367)
        # play button
        self.game.draw_text('Play', self.game.small_font, self.game.white,
                            self.game.window, self.middle_w, 450+(self.button_height/2)-15)

    def set_option_color(self):
        if self.choice_active:
            if self.game.difficulty == 'Easy':
                self.color1 = self.active_color
                self.color2 = self.game.dark_grey
                self.color3 = self.game.dark_grey
            if self.game.difficulty == 'Medium':
                self.color1 = self.game.dark_grey
                self.color2 = self.active_color
                self.color3 = self.game.dark_grey
            if self.game.difficulty == 'Hard':
                self.color1 = self.game.dark_grey
                self.color2 = self.game.dark_grey
                self.color3 = self.active_color
        else:
            self.color1 = self.game.dark_grey
            self.color2 = self.game.dark_grey
            self.color3 = self.game.dark_grey

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.create_menu()
            self.get_click()
            self.check_events()
            pygame.display.update()

    def get_click(self):

        mx, my = pygame.mouse.get_pos()
        if self.play_btn.collidepoint((mx, my)):
            if self.click:
                if self.game.difficulty != 'Solving':
                    # if self.game.username != '':

                    print('Working: play game')
                    self.game.get_diff()
                    self.game.playing = True
                    self.run_display = False
                # self.game.username = 'player'

        # NEED: click event for setting difficulty
        if self.easy_btn.collidepoint((mx, my)):
            if self.click:
                self.game.difficulty = 'Easy'
                self.choice_active = True
                print('Selected easy')
        if self.med_btn.collidepoint((mx, my)):
            if self.click:
                self.game.difficulty = 'Medium'
                self.choice_active = True
                print('Selected medium')
        if self.hard_btn.collidepoint((mx, my)):
            if self.click:
                self.game.difficulty = 'Hard'
                self.choice_active = True
                print('Selected Hard')

        if self.click:
            if self.usr_input.collidepoint((mx, my)):
                self.click_active = True
            else:
                self.click_active = False
        self.click = False

# Transition menu to play/solve again


class AgainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.play_text = 'Play'
        self.solve_text = 'Solve'
        self.mode_text = ''
        self.mode_string = self.mode_text + ' again?'
        self.btn_w = 100
        self.curr_btn = None

    def update_string(self):
        self.mode_string = self.mode_text + ' again?'

    def get_mode(self):
        if self.game.mode == 'solving':
            self.mode_text = self.solve_text
        if self.game.mode == 'playing':
            self.mode_text = self.play_text
        self.update_string()

    def create_menu(self):
        self.get_mode()

        self.game.window.fill(self.game.grey)

        self.game.draw_text(self.mode_string, self.game.title_font, self.game.white,
                            self.game.window, self.middle_w, 200)

        self.yes_btn = pygame.Rect(
            self.middle_w-self.btn_w-10, 300, self.btn_w, self.button_height)
        self.no_btn = pygame.Rect(
            self.middle_w+10, 300, self.btn_w, self.button_height)

        if self.curr_btn == 'y':
            pygame.draw.rect(self.game.window,
                             self.curr_color, self.yes_btn)
        if self.curr_btn == 'n':
            pygame.draw.rect(self.game.window,
                             self.curr_color, self.no_btn)

        self.get_color()

        self.game.draw_text('Yes', self.game.small_font, self.game.white,
                            self.game.window, self.middle_w-(self.btn_w/2)-10, 300+(self.button_height/2)-15)
        self.game.draw_text('No', self.game.small_font, self.game.white,
                            self.game.window, self.middle_w+(self.btn_w/2)+10, 300+(self.button_height/2)-15)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.create_menu()
            self.get_click()
            self.check_events()
            pygame.display.update()

    def get_click(self):

        mx, my = pygame.mouse.get_pos()
        self.curr_btn = ''

        if self.no_btn.collidepoint((mx, my)):
            self.curr_btn = 'n'
            if self.click:
                self.click_active = True
                self.game.running = False
                self.run_display = False
        if self.yes_btn.collidepoint((mx, my)):
            self.curr_btn = 'y'
            if self.click:
                self.curr_btn = 'y'
                self.click_active = True
                self.game.curr_menu = self.game.main_menu
                self.run_display = False

                #self.game.playing = False

        self.click = False
