import random
import pygame


class Particles(pygame.sprite.Sprite):
    def __init__(self, group, pos, direction, lifetime, speed, color) -> None:
        super().__init__(*group)
        self.pos = pos
        self.direction = direction
        self.lifetime = lifetime
        self.speed = speed
        self.color = color

    @staticmethod
    def create_particle(group, pos, color, number=1):
        for _ in range(number):

            Particles(
                group,
                pos,
                direction=pygame.Vector2(
                    random.uniform(-1, 1), random.uniform(-1, 1)),
                lifetime=random.randint(0, 30),
                speed=random.randint(1, 10),
                color=color
            )

    def draw(self, surf: pygame.Surface):
        pygame.draw.circle(surf, self.color, self.pos, self.lifetime // 2)
        surface = pygame.Surface((self.lifetime, self.lifetime))
        pygame.draw.circle(surface, (20, 20, 20),
                           (self.lifetime, (self.lifetime)), self.lifetime)
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
