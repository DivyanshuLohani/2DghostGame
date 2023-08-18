import pygame
from utils import Singleton


class AudioManager(Singleton):

    def __init__(self) -> None:
        pygame.mixer.init()
        self.mixer = pygame.mixer.Channel(0)
        self.muted = False

    def play(self, sound, loops=0):
        if self.muted:
            return
        self.mixer.play(sound, loops)

    def play_fx(self, fx):
        if self.muted:
            return
        fx.play()

    def toggle_mute(self):
        if self.muted:
            self.mixer.set_volume(1)
            self.muted = False
        else:
            self.mixer.set_volume(0)
            self.muted = True
