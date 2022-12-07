
#################
# Soduko Solver #
#################

## Amos Hodges ##


# drafting menu for solver/game

from pygame.locals import *
import pygame
import sys


pygame.init()
pygame.display.set_caption('Sudoku Solver Menu')

#################################################
# TO DO
# write a function to center text within rectangles
# convert to class and tidy up variables
# link game class to  different menus
#
#
# Eventually:
# animation of sudoku board on menu page?

display_width = 540
display_height = 540
screen = pygame.display.set_mode((display_width, display_height))

title_font = pygame.font.SysFont('Corbel', 80)
reg_font = pygame.font.SysFont('Corbel', 20)
smallfont = pygame.font.SysFont('Corbel', 30)

# draw text on screen


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    text_width = textobj.get_width()
    textrect = textobj.get_rect()
    textrect.topleft = (x - (text_width/2), y)
    surface.blit(textobj, textrect)


click = False


button_width = 300
button_height = 50

center_w = (display_width/2) - (button_width/2)
center_h = (display_height/2) - (button_height/2)


def main_menu():

    while True:

        screen.fill((128, 128, 128))

        draw_text('Sudoku Solver', title_font, (255, 255, 255),
                  screen, display_width/2, 20)
        draw_text('by Amos Hodges', reg_font, (255, 255, 255),
                  screen, display_width/2, 100)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(center_w, 200, button_width, button_height)
        button_2 = pygame.Rect(center_w, 300, button_width, button_height)

        pygame.draw.rect(screen, (80, 80, 80), button_1)
        pygame.draw.rect(screen, (80, 80, 80), button_2)

        draw_text('Play Sudoku', smallfont, (255, 255, 255),
                  screen, display_width/2, 200+(button_height/2)-15)
        draw_text('Solve a puzzle for me', smallfont, (255, 255, 255),
                  screen, display_width/2, 300+(button_height/2)-15)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                solve()
        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


def game():
    running = True
    while running:
        screen.fill((128, 128, 128))

        draw_text('Play Sudoku', title_font, (255, 255, 255),
                  screen, display_width/2, 20)
        draw_text('Enter username:', reg_font,
                  (255, 255, 255), screen, display_width/2, 150)
        draw_text('Select Difficulty:', reg_font,
                  (255, 255, 255), screen, display_width/2, 300)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()


def solve():
    running = True
    while running:
        screen.fill((128, 128, 128))

        draw_text('Solver', title_font, (255, 255, 255),
                  screen, display_width/2, 20)
        draw_text('Enter a valid sudoku puzzle', reg_font,
                  (255, 255, 255), screen, display_width/2, 150)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()


main_menu()
