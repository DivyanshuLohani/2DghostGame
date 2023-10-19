import pygame

from utils import get_font

pygame.font.init()
font = pygame.font.Font(None, 30)


def debug(info, x=10, y=10):
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surface, 'Black', debug_rect)
    display_surface.blit(debug_surf, debug_rect)


class UICursor(pygame.sprite.Sprite):
    def __init__(self, groups) -> None:
        super().__init__([groups])

        self.image = pygame.transform.scale(
            pygame.image.load("assets/cursor.png").convert_alpha(),
            (64, 64)
        )
        self.rect = self.image.get_rect()


class Text(pygame.sprite.Sprite):
    def __init__(self, group, text, pos=None, color=None, size=80) -> None:
        super().__init__([group])

        self.font = get_font(size)
        self.txt = text
        if color is None:
            color = "white"
        if pos is None:
            pos = (0, 0)
        self.text = self.font.render(
            text, True, color,
        )
        self.image = self.text
        self.rect = pygame.rect.Rect(
            *pos, self.text.get_width(), self.text.get_height()
        )

    def center(self, window, offset_x=0, offset_y=0):
        width, height = window
        self.rect.topleft = (
            ((width - self.text.get_width()) // 2) + offset_x,
            (height // 2 - self.text.get_height()) + offset_y
        )


class Button(Text):
    def __init__(self, group, text, pos, color=None, size=80) -> None:
        super().__init__(group, text, pos, color, size)
        self.hovering = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovering = self.rect.collidepoint(*mouse_pos)
        if self.hovering:
            surface = pygame.Surface(
                (self.text.get_width(), self.text.get_height())
            )
            surface.blit(self.text, (0, 0))
            self.text = surface
        else:
            self.text = self.font.render(
                self.txt, True, "white"
            )


class BlinkSprite(pygame.sprite.Sprite):
    def __init__(self, groups, pos, image, interval=100) -> None:
        super().__init__([groups])
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.interval = interval
        self.last_time = 0
        self.current_time = pygame.time.get_ticks()
        self.is_draw = True

    def update(self):
        if pygame.time.get_ticks() - self.last_time > self.interval:
            self.is_draw = not self.is_draw
            self.last_time = pygame.time.get_ticks()

    def draw(self, surf):
        if self.is_draw:
            surf.blit(self.image, self.rect)


class BlinkText(BlinkSprite):
    def __init__(self, groups, pos, text, color=None, interval=100, size=32) -> None:
        font = get_font(size)
        color = color or "white"
        self.text = font.render(text, False, color)
        super().__init__(groups, pos, self.text, interval)

    def center(self, window, offset_x=0, offset_y=0):
        width, height = window
        self.rect.topleft = (
            ((width - self.text.get_width()) // 2) + offset_x,
            (height // 2 - self.text.get_height()) + offset_y
        )
