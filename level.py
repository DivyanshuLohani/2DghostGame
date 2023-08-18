import math
from random import uniform, choice, randint
import pygame
from ui import Button, UICursor, debug
from obstacle import Obstacle, PointObstacle
from particles import Particles
from player import Player
from settings import BG_COLOR, DEBUG, WINDOW_HEIGHT, WINDOW_WIDTH
from sprites import ScrollingEnvironment
from audio import AudioManager

pygame.font.init()
pygame.mixer.init()
font = pygame.font.Font("assets/Roboto-Black.ttf", 100)


class Screen:

    def __init__(self, game) -> None:

        self.game = game
        self.camera_grp = CameraGroup()
        self.ui_group = UIGroup()

    def update(self, delta_time):
        pass

    def events(self, event):
        pass

    def draw(self):
        pass


class MainMenu(Screen):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.play_button = Button(self.ui_group, (0, 0), "PLAY")
        self.play_button.center((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.cursor = UICursor([])
        self.game_speed = 1

    def draw(self):
        self.camera_grp.draw(self.game_speed)
        self.ui_group.draw(self.game.screen)
        self.game.screen.blit(self.cursor.image, self.cursor.rect.center)

    def update(self, delta_time):
        self.camera_grp.update(speed=self.game_speed)
        self.ui_group.update()
        self.cursor.update()

    def events(self, event):
        if event.type == pygame.MOUSEMOTION:

            self.cursor.rect.topleft = pygame.mouse.get_pos()
            key = pygame.mouse.get_pressed(3)
            color = "white" if not key[0] else "black"
            Particles.create_particle(
                [self.ui_group], self.cursor.rect.center, color, 1, speed=2
            )
        elif event.type == pygame.MOUSEBUTTONDOWN:

            self.game.level = Level(self.game)


class Level(Screen):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.display_surface = pygame.display.get_surface()
        self.obstacles_sp = pygame.image.load(
            "assets/Obstacle.png"
        ).convert_alpha()
        self.obstacles_sp = pygame.transform.scale(
            self.obstacles_sp,
            (140, 140)
        )
        # Restart Text
        self.r_btn = Button("", (0, 0), "R to Restart")
        self.r_btn.center((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Groups
        self.obstacles = ObstaclesGroup()

        # Player
        self.player = Player(
            [self.camera_grp],
            (100, 250),
            self.obstacles
        )

        # Obstacle Configration
        self.positions = [100, 410, 250]
        self.game_speed = 10

        # Spawn
        self.spawn_interval = 1000
        self.last_spawn = 0
        self.min_spawn = 400

        self.game_running = True

        # Audio
        self.mixer = AudioManager()
        self.bg_music = pygame.mixer.Sound("assets/Background.wav")
        self.mixer.play(self.bg_music, 5)

    def update(self, delta_time):

        self.camera_grp.update(game_speed=self.game_speed)
        self.obstacles.update(game_speed=self.game_speed)

        if pygame.time.get_ticks() - self.last_spawn > self.spawn_interval:
            self.spawn()
            self.last_spawn = pygame.time.get_ticks()
            if self.spawn_interval > self.min_spawn:
                self.spawn_interval -= 10

        if self.player.lives <= 0:
            self.game_running = False
            self.player.kill()
            if self.mixer.muted:
                return
            for i in range(10, 3, -1):
                self.mixer.mixer.set_volume(i/10)

        if randint(0, 1000) == 10:
            pos = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))
            # for i in range(randint(10, 100)):
            Particles(
                [self.camera_grp],
                pos,
                direction=pygame.Vector2(
                    uniform(-1, 1), uniform(-1, 1)),
                lifetime=100,
                speed=0.2,
                color="black",
                radius=10,
                reduce_with_lifetime=False
            )

    def draw(self):
        self.camera_grp.draw(self.game_speed)
        self.player.draw_ui()
        if not self.game_running:
            self.display_surface.blit(self.r_btn.image, self.r_btn.rect)
        if DEBUG:
            self.obstacles.draw()

    def events(self, event):

        if self.game_running:
            self.player.input(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if not self.game_running:
                    self.game_running = True
                    [sprite.kill() for sprite in self.obstacles.sprites()]
                    self.player = Player(
                        [self.camera_grp], (100, 250), self.obstacles
                    )
                    self.mixer.mixer.set_volume(1)
                    self.mixer.play(self.bg_music, True)
                    self.spawn_interval = 1000
            if event.key == pygame.K_m:
                self.mixer.toggle_mute()

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
        # self.cam_shake_smooth = 3
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
