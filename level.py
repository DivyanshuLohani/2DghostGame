import math
from random import uniform, choice
import pygame
from button import Button
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

        # Groups
        self.camera_grp = CameraGroup()
        self.obstacles = ObstaclesGroup()
        self.ui_group = UIGroup()

        # UI
        self.play_button = Button(self.ui_group, (0, 0), "PLAY")
        self.play_button.rect.topleft = (
            WINDOW_WIDTH // 2 - self.play_button.text.get_width() // 2, WINDOW_HEIGHT // 2 -
            self.play_button.text.get_height()
        )

        # Player
        self.player = Player([self.camera_grp], (100, 250), self.obstacles)

        # Assets
        obstacles_sp = pygame.image.load(
            "assets/Obstacle.png").convert_alpha()

        # Obstacle Configration
        self.obstacles_sp = pygame.transform.scale(obstacles_sp, (140, 140))
        self.positions = [100, 410, 250]
        self.game_speed = 10

        # Spawn
        self.spawn_interval = 1000
        self.last_spawn = 0
        self.min_spawn = 400

        self.game_running = True

        # Audio
        self.mixer = pygame.mixer.Channel(0)
        self.bg_music = pygame.mixer.Sound("assets/Background.wav")
        self.mixer.play(self.bg_music, 5)

        self.game_started = False

        # Cursor
        self.cursor = pygame.transform.scale(
            pygame.image.load("assets/cursor.png").convert_alpha(),
            (64, 64)
        )
        self.cursor_rect = self.cursor.get_rect()

    def run(self):

        if not self.game_started:
            self.main_menu()
            return
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

        if self.player.lives <= 0:
            self.game_running = False
            self.player.kill()
            if self.player.mute_audio:
                return
            for i in range(10, 3, -1):
                self.mixer.set_volume(i/10)

    def events(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                if not self.game_started:
                    key = pygame.mouse.get_pressed(3)
                    color = "white" if not key[0] else "black"
                    Particles.create_particle(
                        [self.ui_group], self.cursor_rect.topleft, color, 1, speed=2
                    )
            if self.game_running:
                self.player.input(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.hovering:
                    self.game_started = True
                    self.play_button.hovering = False
                    self.mixer.play(self.bg_music, 5)
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
                if event.key == pygame.K_m:
                    if self.player.mute_audio:
                        self.player.mute_audio = False
                        self.mixer.set_volume(1)
                    else:
                        self.player.mute_audio = True
                        self.mixer.set_volume(0)

    def spawn(self):
        if not self.game_running:
            return
        pos = choice(self.positions)
        PointObstacle([self.obstacles], (WINDOW_WIDTH + 400, pos))
        for i in self.positions:
            if i != pos:
                Obstacle([self.camera_grp, self.obstacles], self.obstacles_sp,
                         (WINDOW_WIDTH + 400, i))

    def main_menu(self):
        self.display_surface.fill(BG_COLOR)
        self.camera_grp.draw_bg(self.display_surface, self.game_speed)
        self.ui_group.update()
        self.ui_group.draw(self.display_surface)

        mouse_pos = pygame.mouse.get_pos()
        self.cursor_rect.center = mouse_pos
        self.display_surface.blit(self.cursor, self.cursor_rect)


class CameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2(100, 200)

        self.background = pygame.image.load(
            "assets/Environment.png").convert_alpha()
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
        self.save = False

    def camera_shake(self, duration=5):
        self.cam_shake_time = duration
        self.camera_shaking = True

    def draw_bg(self, surface, speed):
        for i, sp in enumerate(self.bgs):
            if i == 0 or i == 3:
                sp.speed = speed
            sp.draw(surface)

    def draw(self, speed) -> None:
        self.surface.fill(BG_COLOR)
        self.draw_bg(self.surface, speed)

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


class UIGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()

    def draw(self, surface):
        for sprite in self.sprites():
            if isinstance(sprite, Particles):
                sprite.draw(surface)
            elif isinstance(sprite, Button):
                surface.blit(sprite.text, sprite.rect)
            else:
                surface.blit(sprite.image, sprite.rect)
