import pygame
from config import show_menu
from game import run_game

def main():
    pygame.init()
    config = show_menu()
    run_game(config)
    pygame.quit()

if __name__ == "__main__":
    main()
