import pygame
import gameconfig as gc

class Bomb(pygame.sprite.Sprite):
    def __init__(self, game, image_list, group, row_number, column_number, size):
        super().__init__(group)

        self.game = game
        self.y_offset = gc.Y_OFFSET

        self.row = row_number
        self.column = column_number

        self.size = size

        self.x = self.column * self.size
        self.y = (self.row * self.size) + self.y_offset

        self.image_list = image_list
        self.image_index = 0
        self.image = self.image_list[self.image_index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))