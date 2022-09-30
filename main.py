import sys
import pygame
from settings import BG_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH, FPS
from level import Level


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Shooter Game")
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:

            self.level.run()

            pygame.display.update()

            self.clock.tick(FPS)


if __name__ == "__main__":
    g = Game()
    g.run()
