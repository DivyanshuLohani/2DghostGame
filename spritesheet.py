import pygame

from settings import ACTUAL_TILE_SIZE, TILE_SIZE


class SpriteSheet:
    def __init__(self, path, width=ACTUAL_TILE_SIZE, height=ACTUAL_TILE_SIZE) -> None:
        self.image = pygame.image.load(path).convert_alpha()
        self.sprite_width = width
        self.sprite_height = height
        self.no_sprites_in_column = (
            self.image.get_height() // self.sprite_height)
        self.no_sprites_in_row = (
            self.image.get_width() // self.sprite_width)
        self.total_sprites = self.no_sprites_in_column * self.no_sprites_in_row
        self.path = path

    def get_sprite(self, x, y, width, height, scale):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.blit(self.image, (0, 0), (x, y, width, height))
        surface = pygame.transform.scale(surface, (scale, scale))
        return surface

    def get_sprite_by_id(self, id, scale=TILE_SIZE):

        col = 0
        row = 0
        x = -1
        for i in range(self.no_sprites_in_column):
            for j in range(self.no_sprites_in_row):
                x += 1
                if x == id:
                    col = i
                    row = j
                    break
            if x == id:
                break
        return self.get_sprite((row) * ACTUAL_TILE_SIZE, col * ACTUAL_TILE_SIZE, self.sprite_width, self.sprite_height, scale)

    def load_anim(self, num_frames, start, incriment=4):
        end = start + (num_frames - 1) * incriment
        return [self.get_sprite_by_id(i) for i in range(start, end + 1, incriment)]
