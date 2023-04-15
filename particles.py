import random
import pygame


class Particles(pygame.sprite.Sprite):
    def __init__(self, group, pos, direction, lifetime, speed, color, radius=None, reduce_with_lifetime=True) -> None:
        super().__init__(*group)
        self.pos = pos
        self.direction = direction
        self.lifetime = lifetime
        self.speed = speed
        self.color = color
        self.radius = radius or lifetime // 2
        self.reduce_with_lifetime = reduce_with_lifetime

    @staticmethod
    def create_particle(group, pos, color, number=1, speed=None):
        for _ in range(number):

            Particles(
                group,
                pos,
                direction=pygame.Vector2(
                    random.uniform(-1, 1), random.uniform(-1, 1)),
                lifetime=random.randint(0, 30),
                speed=random.randint(1, speed or 10),
                color=color
            )

    def draw(self, surf: pygame.Surface):
        if self.reduce_with_lifetime:
            self.radius = self.lifetime

        pygame.draw.circle(surf, self.color, self.pos, self.radius)
        surface = pygame.Surface((self.radius, self.radius))
        pygame.draw.circle(surface, (20, 20, 20),
                           (self.pos), self.radius)
        surface.set_colorkey((0, 0, 0))
        surf.blit(surface,
                  (
                      self.pos[0] - self.lifetime // 2,
                      self.pos[1] - self.lifetime // 2),
                  special_flags=pygame.BLEND_RGBA_ADD
                  )
        self.lifetime -= 0.5

        self.pos += self.direction * self.speed
        if self.lifetime <= 0:
            self.kill()
