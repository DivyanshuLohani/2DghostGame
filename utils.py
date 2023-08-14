import os
from sys import platform
import pygame

from settings import PACKAGE_NAME

pygame.font.init()


def get_font(size):
    return pygame.font.Font("assets/Roboto-Black.ttf", size)
