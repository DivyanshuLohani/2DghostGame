import os
from sys import platform
import pygame


pygame.font.init()


def get_font(size):
    return pygame.font.Font("assets/Roboto-Black.ttf", size)
