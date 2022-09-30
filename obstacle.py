import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups, image: pygame.Surface, pos) -> None:
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, *args, **kwargs) -> None:
        self.rect.topleft -= pygame.Vector2(kwargs.get("game_speed"), 0)
        if self.rect.topright[0] < 0:
            self.kill()


class PointObstacle(pygame.sprite.Sprite):
    def __init__(self, groups, pos) -> None:
        super().__init__(*groups)
        surface = pygame.Surface((140, 140))
        self.rect = surface.get_rect(topleft=pos)

    def update(self, *args, **kwargs) -> None:
        self.rect.topleft -= pygame.math.Vector2(
            kwargs.get("game_speed") * 2, 0)
        if self.rect.topright[0] < 0:
            self.kill()
