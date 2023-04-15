import sys
import pygame
from settings import WINDOW_HEIGHT, WINDOW_WIDTH, FPS
from level import MainMenu


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
        self.level = MainMenu(self)

    def run(self):
        while True:
            events = pygame.event.get()
            self.level.draw()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.level.events(event)
            self.level.update(1/FPS)

            pygame.display.update()

            self.clock.tick(FPS)


if __name__ == "__main__":
    g = Game()
    g.run()
