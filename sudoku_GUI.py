#################
# Soduko Solver #
#################

## Amos Hodges ##

# GUI created using validate and solve functions

import pygame
from sudoku_solver import check_valid, solve_board
import time
pygame.font.init()


class Grid:

    # next step: write method to randomly generate solvable states
    # allow user to enter a board manually to solve, or select from ease, medium, hard


def main():

    window = pygame.display.set_mode((500, 600))
    pygame.display.set_caption("Sudoku Solver")


if __name__ == '__main__':
    main()
