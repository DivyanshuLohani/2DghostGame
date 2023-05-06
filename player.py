import pygame
from obstacle import PointObstacle
from particles import Particles
from settings import WINDOW_HEIGHT, WINDOW_WIDTH, SCALE_FACTOR
from ui import BlinkSprite

from spritesheet import SpriteSheet

pygame.font.init()
font = pygame.font.Font("assets/Roboto-Black.ttf", 60)


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, pos, obstacles) -> None:
        super().__init__(groups)
        self.sprite_sheet = SpriteSheet("assets/Ghost.png")
        self.anims = [
            self.sprite_sheet.get_sprite(130, 100, 520, 540, SCALE_FACTOR),
            self.sprite_sheet.get_sprite(900, 100, 520, 540, SCALE_FACTOR),
            self.sprite_sheet.get_sprite(130, 860, 520, 540, SCALE_FACTOR),
            self.sprite_sheet.get_sprite(900, 860, 520, 580, SCALE_FACTOR),
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
        self.mute_audio = False
        self.mute_image = pygame.transform.scale(
            pygame.image.load("assets/mute.png"), (64, 64))

        # God Mode
        self.god_mode = False
        self.god_mode_image = pygame.transform.scale(
            pygame.image.load("assets/godmode.jpg"),
            (50, 50)
        )

        # UI
        self.lives_txt = font.render(f"{self.lives}", True, "white")
        self.lives_blink = BlinkSprite(
            "",
            ((WINDOW_WIDTH - self.lives_txt.get_width()) - 30, 10),
            self.lives_txt,
            500
        )

    def input(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                if not self.rect.topleft[1] == self.min_y:
                    Particles.create_particle(
                        self.groups(), self.rect.center, "white", 30)
                    self.rect.topleft -= pygame.Vector2(0, 150)
                    self.groups()[0].camera_shake()

            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                if not self.rect.topleft[1] == self.max_y:
                    Particles.create_particle(
                        self.groups(), self.rect.center, "white", 30)
                    self.rect.topleft += pygame.Vector2(0, 150)
                    self.groups()[0].camera_shake()

            if event.key == pygame.K_g:
                self.god_mode = not self.god_mode

    def collison(self):
        for sprite in self.obstacles.sprites():
            if not self.rect.colliderect(sprite.rect):
                continue

            sprite.kill()
            if isinstance(sprite, PointObstacle):
                self.points += 2
                if self.points % 50 == 0:
                    if not self.mute_audio:
                        self.point_sound.play()

            else:
                Particles.create_particle(
                    self.groups(), self.rect.center, "black", 50)
                self.groups()[0].camera_shake()
                if not self.mute_audio:
                    self.hit_sound.play(fade_ms=100)
                if not self.god_mode:
                    self.lives -= 1
                    self.lives_txt = font.render(
                        f"{self.lives}", True, "white")

    def animate(self):
        self.frame += 0.09
        if self.frame >= len(self.anims) - 1:
            self.frame = 0
        self.image = self.anims[int(self.frame)]

    def draw_ui(self):
        score_txt = font.render(f"{self.points}", True, "white")

        self.display_surface.blit(score_txt, (30, 10))

        if self.lives == 1:
            self.lives_blink.image = self.lives_txt
            self.lives_blink.update()
            self.lives_blink.draw(self.display_surface)
        else:
            self.display_surface.blit(
                self.lives_txt, ((WINDOW_WIDTH - self.lives_txt.get_width()) - 30, 10))

        if self.god_mode:
            self.display_surface.blit(
                self.god_mode_image,
                (WINDOW_WIDTH // 2, 10)
            )
        if self.mute_audio:
            self.display_surface.blit(
                self.mute_image, (30, WINDOW_HEIGHT - (self.mute_image.get_width() + 20)))

    def update(self, *args, **kwargs) -> None:
        self.animate()
        self.collison()
