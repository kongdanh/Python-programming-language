from game import run_game
import sys
import pygame.freetype
sys.stdout.reconfigure(encoding='utf-8')


if __name__ == "__main__":
    pygame.init()
    pygame.freetype.init()
    run_game()
