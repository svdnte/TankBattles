from functions import *
from explosion import Explosion


class Bullet(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image(bullet_image, color_key=-1), (TILE_SIZE / 9, TILE_SIZE / 3))

    def __init__(self, owner: pygame.sprite.Sprite, direction: str, x: int, y: int, all_sprites, bullet_sprites,
                 obstacle_sprites, tank_sprites, player_sprites, explosion_sprites,
                 fast=False, through=False, slow=False, weak=False):
        super().__init__(all_sprites, bullet_sprites)

        self.owner = owner
        self.direction = direction

        self.all_sprites = all_sprites
        self.obstacle_sprites = obstacle_sprites
        self.tank_sprites = tank_sprites
        self.player_sprites = player_sprites
        self.explosion_sprites = explosion_sprites

        self.through = through
        self.weak = weak

        self.image = Bullet.image
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        V = TILE_SIZE * 6 / FPS
        V *= 1.5 if fast else 1
        V *= 0.8 if slow else 1

        if self.direction == 'N':
            self.rect = self.image.get_rect().move(x, y)
            self.rect = self.rect.move(self.owner.rect.w // 2 - 2, -self.h)

            self.vx, self.vy = 0, -V

        elif self.direction == 'E':
            self.image = pygame.transform.rotate(self.image, 270)
            self.rect = self.image.get_rect().move(x, y)
            self.rect = self.rect.move(self.owner.rect.w, self.owner.rect.h // 2 - 2)

            self.vx, self.vy = V, 0

        elif self.direction == 'S':
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect().move(x, y)
            self.rect = self.rect.move(self.owner.rect.w // 2 - 2, self.owner.rect.h)

            self.vx, self.vy = 0, V

        elif self.direction == 'W':
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect().move(x, y)
            self.rect = self.rect.move(-self.h, self.owner.rect.h // 2 - 2)

            self.vx, self.vy = -V, 0

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        self.vx, self.vy = self.vx * 0.998, self.vy * 0.998

        self.check_collide()

    def check_collide(self):
        for sprite in self.obstacle_sprites:
            if pygame.sprite.collide_mask(self, sprite):
                if not self.weak:
                    sprite.hit()
                if not self.through:
                    self.kill()

        if not 0 < self.rect.x < HEIGHT + self.w or not 0 < self.rect.y < HEIGHT + self.h:
            Explosion(self.rect.x, self.rect.y, self.all_sprites,
                      self.explosion_sprites, centered=True, scale=1)
            self.kill()

        for sprite in self.tank_sprites:
            if pygame.sprite.collide_mask(self, sprite):
                self.owner.bullet_hit(sprite)
                sprite.destroy()
                if self.player_sprites.has(sprite):
                    sprite.game_over = True

                if not self.through:
                    self.kill()
