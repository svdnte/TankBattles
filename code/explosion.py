from functions import *
from support import *


class Explosion(pygame.sprite.Sprite):
    image = load_image(explosion_image, -1)

    def __init__(self, x, y, all_sprites, explosion_sprites, centered=False, scale=1):
        super().__init__(all_sprites, explosion_sprites)
        self.rows, self.columns = 9, 9
        self.frames = []
        self.scalee = scale

        self.cut_sheet()
        self.current_frame = 0
        self.current_image = self.frames[self.current_frame]


        if not centered:
            self.rect = self.rect.move(x, y)
        else:
            self.rect.x = x - self.rect.w // 4
            self.rect.y = y - self.rect.h // 4

    def cut_sheet(self):
        self.rect = pygame.Rect(0, 0, Explosion.image.get_width() // self.columns,
                                Explosion.image.get_height() // self.rows)

        for j in range(self.rows):
            for i in range(self.columns):
                frame_location = self.rect.w * i, self.rect.h * j
                subsurface = Explosion.image.subsurface(pygame.Rect(frame_location, self.rect.size))
                subsurface = pygame.transform.scale(subsurface, (TILE_SIZE * self.scalee, TILE_SIZE * self.scalee) )
                self.frames.append(subsurface)

    def update(self):
        self.current_frame += 1
        self.image = self.frames[self.current_frame]

        if self.current_frame == len(self.frames) - 1:
            self.kill()
