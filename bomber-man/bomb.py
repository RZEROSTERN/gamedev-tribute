import pygame
import gameconfig as gc
from explosion import Explosion

class Bomb(pygame.sprite.Sprite):
    def __init__(self, game, image_list, group, power, row_number, column_number, size, remote):
        super().__init__(group)

        self.game = game
        self.row = row_number
        self.column = column_number

        self.size = size
        self.x = self.column * self.size
        self.y = (self.row * self.size) + gc.Y_OFFSET

        self.bomb_counter = 1
        self.bomb_timer = 12
        self.passable = True
        self.remote = remote
        self.power = power

        self.image_index = 0
        self.image_list = image_list
        self.image = self.image_list[self.image_index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.animation_length = len(self.image_list)
        self.animation_frame_time = 200
        self.animation_timer = pygame.time.get_ticks()

        self.insert_bomb_into_grid()

    def update(self):
        self.animation()
        self.planted_bomb_after_collision()

        if self.bomb_counter == self.bomb_timer and not self.remote:
            self.explode()

    def draw(self, window, offset):
        window.blit(self.image, (self.rect.x - offset, self.rect.y))

    def insert_bomb_into_grid(self):
        self.game.level_matrix[self.row][self.column] = self
        self.game.player.bombs_planted += 1

    def animation(self):
        if pygame.time.get_ticks() - self.animation_timer >= self.animation_frame_time:
            self.image_index += 1
            self.image_index = self.image_index % self.animation_length
            self.image = self.image_list[self.image_index]
            self.animation_timer = pygame.time.get_ticks()
            self.bomb_counter += 1

    def remove_bomb_from_grid(self):
        self.game.level_matrix[self.row][self.column] = "_"
        self.game.player.bombs_planted -= 1

    def explode(self):
        self.remove_bomb_from_grid()
        Explosion(self.game, self.game.assets.explosions, "center", self.power, self.game.groups["explosions"], self.row, self.column, self.size)
        self.kill()

    def planted_bomb_after_collision(self):
        if not self.passable:
            return
        if not self.rect.colliderect(self.game.player):
            self.passable = False

    def __repr__(self):
        return "'!'"

