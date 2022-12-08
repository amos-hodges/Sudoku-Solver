#################
# Soduko Solver #
#################

## Amos Hodges ##

## menu classes #

import pygame


class Menu():

    def __init__(self, game):
        self.game = game
        self.middle_w = self.game.display_width / 2
        self.middle_h = self.game.display_height / 2
        self.button_width = 300
        self.button_height = 50
        self.center_w = self.middle_w - (self.button_width/2)
        # initialize fonts in game class
        self.click = False
        self.run_display = True

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
                # print('thisworks')
                self.run_display = False
            if self.solve_puz_btn.collidepoint((mx, my)):
                #print('this does too')
                self.run_display = False
                self.game.playing = True
        self.click = False


# Enter username / select difficulty


class DiffMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def create_menu(self):

        self.game.window.fill(self.game.grey)

        self.game.draw_text('Enter Username', self.game.title_font, self.game.white,
                            self.game.window, self.middle_w, 20)
        # Need text input to be stored
        self.play_btn = pygame.Rect(
            self.center_w, 300, self.button_width, self.button_height)

        pygame.draw.rect(self.game.window, self.game.dark_grey, self.play_btn)

        self.game.draw_text('Play', self.game.small_font, self.game.white,
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
        if self.play_btn.collidepoint((mx, my)):
            if self.click:
                print('Working: play game')
                self.game.playing = True
                self.run_display = False
        self.click = False
