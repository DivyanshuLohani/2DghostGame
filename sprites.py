import math
import pygame

from settings import WINDOW_HEIGHT, WINDOW_WIDTH


class ScrollingEnvironment:
    def __init__(self, image, scale=None, speed=5, alpha=None, flipped=False) -> None:
        self.background = image
        if scale:
            self.background = pygame.transform.scale(
                self.background, (self.background.get_width(), scale))
        if alpha:
            self.background.set_alpha(alpha)
        self.flipped = flipped
        if flipped:
            self.background = pygame.transform.flip(
                self.background, False, True)

        self.bg_width = self.background.get_width()
        self.bg_tiles = math.ceil(self.bg_width / WINDOW_WIDTH)
        self.speed = speed
        self.scroll = 0

    def draw(self, surface):
        for i in range(self.bg_tiles):
            y = WINDOW_HEIGHT - self.background.get_height()
            if self.flipped:
                y = 0

            surface.blit(
                self.background, [i * self.bg_width + self.scroll, y])
        self.scroll -= self.speed
        if abs(self.scroll) > self.bg_width:
            self.scroll = 0
