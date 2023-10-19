import os
from sys import platform
import pygame


pygame.font.init()


def check_highscore(force=False):
    # Check if file exists
    # Windows only
    base = os.getenv("APPDATA")
    path = os.path.join(base, "GhostGame")
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = os.path.join(path, "score.dat")
    if force or not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("0")
    return file_path


def read_hiscore():
    file_path = check_highscore()
    with open(file_path, "r") as f:
        score = f.read()
        if not score.isdigit() or "." in score:  # Check float
            score = 0
            # File is couupt
            check_highscore(True)
        else:
            score = int(score)

    return score


def save_hiscore(score):
    file_path = check_highscore()
    with open(file_path, "w") as f:
        f.write(str(score))

    return score


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
