import pygame
import gameconfig as gc

class Blocks(pygame.sprite.Sprite):
    def __init__(self, game, images, group, row_number, column_number, size):
        super().__init__(group)

        self.game = game
        self.y_offset = gc.Y_OFFSET

        self.row = row_number
        self.column = column_number

        self.size = size

        self.x = self.column * self.size
        self.y = (self.row * self.size) + self.y_offset

        self.passable = False
        self.image_list = images
        self.image_index = 0
        self.image = self.image_list[self.image_index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        pass

    def draw(self, window):
        window.blit(self.image, self.rect)
        
    def __repr__(self):
        return "'#'"
    
class HardBlock(Blocks):
    def __init__(self, game, images, group, row_number, column_number, size):
        super().__init__(game, images, group, row_number, column_number, size)

class SoftBlock(Blocks):
    def __init__(self, game, images, group, row_number, column_number, size):
        super().__init__(game, images, group, row_number, column_number, size)
        self.passable = True

    def __repr__(self):
        return "'@'"