import random
import pygame
from settings import PARTICLES_POOL_SIZE


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
        for i in range(number):

            while PARTICLES[i].lifetime > 0:
                i += 1
                if i > len(PARTICLES) - 1:
                    break
            if i == len(PARTICLES):
                break
            PARTICLES[i].add([group])
            PARTICLES[i].pos = pos
            PARTICLES[i].direction = pygame.Vector2(
                random.uniform(-1, 1),
                random.uniform(-1, 1)
            )
            PARTICLES[i].lifetime = random.randint(0, 30)
            PARTICLES[i].speed = random.randint(1, speed or 10)
            PARTICLES[i].color = color

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
            self.remove(self.groups())


PARTICLES = [
    Particles("", (0, 0), (0, 0), 0, 0, (255, 255, 255))
    for _ in range(PARTICLES_POOL_SIZE)
]
