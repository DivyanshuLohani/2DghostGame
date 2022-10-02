import pygame
pygame.font.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
ACTUAL_TILE_SIZE = 16
TILE_SIZE = 64
FPS = 60
BG_COLOR = "#575757"
DEBUG = False


def get_font(size):
    return pygame.font.Font("assets/Roboto-Black.ttf", size)
