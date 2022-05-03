import pygame
from src import controller


def update():
    pygame.display.updated()
    pygame.time.Clock().tick


def main():
    main_window = controller.Controller()
    main_window.mainLoop()


main()
