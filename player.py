import pygame
from obstacle import PointObstacle
from particles import Particles
from settings import WINDOW_WIDTH

from spritesheet import SpriteSheet

pygame.font.init()
font = pygame.font.Font("assets/Roboto-Black.ttf", 60)


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, pos, obstacles) -> None:
        super().__init__(groups)
        self.sprite_sheet = SpriteSheet("assets/Ghost.png")
        self.anims = [
            self.sprite_sheet.get_sprite(130, 100, 520, 540, 150),
            self.sprite_sheet.get_sprite(900, 100, 520, 540, 150),
            self.sprite_sheet.get_sprite(130, 860, 520, 540, 150),
            self.sprite_sheet.get_sprite(900, 860, 520, 580, 150),
        ]
        self.frame = 0
        self.image = self.anims[self.frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.max_y = 400
        self.min_y = 100
        self.obstacles = obstacles
        self.display_surface = pygame.display.get_surface()

        self.lives = 3
        self.points = 0

        # Sounds
        self.point_sound = pygame.mixer.Sound("assets/point.wav")
        self.hit_sound = pygame.mixer.Sound("assets/hit.wav")

        # God Mode
        self.god_mode = False

    def input(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if not self.rect.topleft[1] == self.min_y:
                    self.rect.topleft -= pygame.Vector2(0, 150)
                    self.groups()[0].camera_shake()
                    Particles.create_particle(
                        self.groups(), self.rect.center, "white", 30)

            if event.key == pygame.K_s:
                if not self.rect.topleft[1] == self.max_y:
                    self.rect.topleft += pygame.Vector2(0, 150)
                    self.groups()[0].camera_shake()
                    Particles.create_particle(
                        self.groups(), self.rect.center, "white", 30)

            if event.key == pygame.K_g:
                self.god_mode = not self.god_mode

    def collison(self):
        for sprite in self.obstacles.sprites():
            if not self.rect.colliderect(sprite.rect):
                continue

            sprite.kill()
            if isinstance(sprite, PointObstacle):
                self.points += 2
            else:
                Particles.create_particle(
                    self.groups(), self.rect.center, "black", 50)
                self.groups()[0].camera_shake()
                self.hit_sound.play(fade_ms=100)
                if not self.god_mode:
                    self.lives -= 1

    def animate(self):
        self.frame += 0.09
        if self.frame >= len(self.anims) - 1:
            self.frame = 0
        self.image = self.anims[int(self.frame)]

    def ui(self):
        score_txt = font.render(f"{self.points}", True, "white")
        lives_txt = font.render(f"{self.lives}", True, "white")
        self.display_surface.blit(score_txt, (30, 10))
        self.display_surface.blit(
            lives_txt, ((WINDOW_WIDTH - lives_txt.get_width()) - 30, 10))
        if self.god_mode:
            pygame.draw.rect(self.display_surface, "green",
                             (WINDOW_WIDTH // 2, 10, 50, 50))

    def update(self, *args, **kwargs) -> None:
        self.animate()
        self.collison()
