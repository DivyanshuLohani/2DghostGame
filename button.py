import pygame

from settings import get_font


class Button(pygame.sprite.Sprite):
    def __init__(self, group, pos, text, size=80) -> None:
        super().__init__([group])
        self.font = get_font(size)
        self.txt = text
        self.text = self.font.render(
            text, True, "white"
        )
        self.image = self.text
        self.rect = pygame.rect.Rect(
            *pos, self.text.get_width(), self.text.get_height()
        )
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
