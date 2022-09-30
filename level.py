import math
from random import uniform, choice
import pygame
from obstacle import Obstacle, PointObstacle
from particles import Particles
from player import Player

from settings import BG_COLOR, DEBUG, WINDOW_HEIGHT, WINDOW_WIDTH
from sprites import ScrollingEnvironment
pygame.font.init()
pygame.mixer.init()
font = pygame.font.Font("assets/Roboto-Black.ttf", 100)


class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.camera_grp = CameraGroup()
        self.obstacles = ObstaclesGroup()
        self.player = Player([self.camera_grp], (100, 250), self.obstacles)
        obstacles_sp = pygame.image.load(
            "assets\\Obstacle.png").convert_alpha()
        self.obstacles_sp = pygame.transform.scale(obstacles_sp, (140, 140))
        self.positions = [100, 410, 250]
        self.game_speed = 10

        self.spawn_interval = 1000
        self.last_spawn = 0
        self.min_spawn = 400

        self.game_running = True

        self.mixer = pygame.mixer.Channel(0)
        self.bg_music = pygame.mixer.Sound("assets/Background.wav")
        self.mixer.play(self.bg_music)

    def run(self):
        self.camera_grp.update(game_speed=self.game_speed)
        self.camera_grp.draw(self.game_speed)
        self.player.ui()
        if self.game_running:
            self.obstacles.update(game_speed=self.game_speed)
        else:
            txt = font.render("R To RESTART", True, "white")
            self.display_surface.blit(
                txt,
                (WINDOW_WIDTH // 2 - txt.get_width() // 2,
                 WINDOW_HEIGHT // 2 - txt.get_height() // 2)
            )
        if DEBUG:
            self.obstacles.draw()

        if pygame.time.get_ticks() - self.last_spawn > self.spawn_interval:
            self.spawn()
            self.last_spawn = pygame.time.get_ticks()
            if self.spawn_interval > self.min_spawn:
                self.spawn_interval -= 10

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if self.game_running:
                self.player.input(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if not self.game_running:
                        self.game_running = True
                        [sprite.kill() for sprite in self.obstacles.sprites()]
                        self.player = Player(
                            [self.camera_grp], (100, 250), self.obstacles)
                        self.mixer.set_volume(1)
                        self.mixer.play(self.bg_music, True, fade_ms=1000)
                        self.spawn_interval = 1000

        if self.player.lives <= 0:
            self.game_running = False
            self.player.kill()

            for i in range(10, 3, -1):
                self.mixer.set_volume(i/10)

    def spawn(self):
        if not self.game_running:
            return
        pos = choice(self.positions)
        PointObstacle([self.obstacles], (WINDOW_WIDTH + 400, pos))
        for i in self.positions:
            if i != pos:
                Obstacle([self.camera_grp, self.obstacles], self.obstacles_sp,
                         (WINDOW_WIDTH + 400, i))


class CameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2(100, 200)

        self.background = pygame.image.load(
            "assets\\Environment.png").convert_alpha()
        self.background.fill((0, 0, 0), None, pygame.BLEND_RGBA_MULT)
        self.bgs = [
            # Bottom
            ScrollingEnvironment(self.background, 120, 5, 255),
            ScrollingEnvironment(self.background, 230, 3, 155),
            ScrollingEnvironment(self.background, 320, 1, 100),

            # TOP
            ScrollingEnvironment(self.background, 120, 5, 255, True),
            ScrollingEnvironment(self.background, 230, 3, 155, True),
            ScrollingEnvironment(self.background, 320, 1, 100, True),
        ]
        self.camera_shaking = False
        self.cam_shake_time = 5
        self.cam_shake_strength = 10

    def camera_shake(self, duration=5):
        self.cam_shake_time = duration
        self.camera_shaking = True

    def draw(self, speed) -> None:
        self.surface.fill(BG_COLOR)
        for i, sp in enumerate(self.bgs):
            if i == 0 or i == 3:
                sp.speed = speed
            sp.draw(self.surface)

        for sprite in reversed(self.sprites()):
            if isinstance(sprite, Particles):
                sprite.draw(self.surface)
            else:
                self.surface.blit(sprite.image, sprite.rect)

        if self.camera_shaking:
            self.cam_shake_time -= 1
            pos = pygame.Vector2(
                uniform(-1, 1), uniform(-1, 1)) * self.cam_shake_strength
            if self.cam_shake_time <= 0:
                self.camera_shaking = False
        else:
            pos = (0, 0)

        self.display_surface.blit(self.surface, pos)


class ObstaclesGroup(pygame.sprite.Group):

    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def draw(self):
        for sprite in self.sprites():
            if isinstance(sprite, Obstacle):
                pygame.draw.rect(self.display_surface, "red", sprite.rect)
            else:
                pygame.draw.rect(self.display_surface, "green", sprite.rect)
