import os
from sys import platform
import pygame


pygame.font.init()


def get_font(size):
    return pygame.font.Font("assets/Roboto-Black.ttf", size)


def get_path(file):
    win = get_platform()
    if win == 'android':
        return


def get_platform():
    if 'ANDROID_ARGUMENT' in os.environ:
        return "android"
    elif platform in ['linux', 'linux2', 'linux3']:
        return "linux"
    elif platform in ['win32', 'cygwin']:
        return "win"
    else:
        raise TypeError("Undefined Platform")


class Singleton:
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance
