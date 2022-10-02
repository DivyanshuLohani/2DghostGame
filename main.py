import sys
import pygame
from settings import BG_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH, FPS
from level import Level


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.mouse.set_cursor(
            (8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
        pygame.display.set_caption("Ghost Runner")
        pygame.display.set_icon(pygame.image.load(
            "assets/Obstacle.png"))
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.level.run()
            self.level.events(events)

            pygame.display.update()

            self.clock.tick(FPS)


if __name__ == "__main__":
    g = Game()
    g.run()
