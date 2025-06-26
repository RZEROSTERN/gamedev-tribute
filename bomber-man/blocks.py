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

    def draw(self, window, offset):
        window.blit(self.image, (self.rect.x - offset, self.rect.y))
        
    def __repr__(self):
        return "'#'"
    
class HardBlock(Blocks):
    def __init__(self, game, images, group, row_number, column_number, size):
        super().__init__(game, images, group, row_number, column_number, size)

class SoftBlock(Blocks):
    def __init__(self, game, images, group, row_number, column_number, size):
        super().__init__(game, images, group, row_number, column_number, size)

        self.animation_timer = pygame.time.get_ticks()
        self.animation_frame_rate = 50
        self.destroyed = False

    def update(self):
        if self.destroyed:
            if pygame.time.get_ticks() - self.animation_timer >= self.animation_frame_rate:
                self.image_index += 1
                if self.image_index == len(self.image_list):
                    self.kill()
                    return
                
                self.image = self.image_list[self.image_index]
                self.animation_timer = pygame.time.get_ticks()

    def destroy_soft_block(self):
        if not self.destroyed:
            self.animation_timer = pygame.time.get_ticks()
            self.destroyed = True
            self.game.level_matrix[self.row][self.column] = "_"
            return

    def __repr__(self):
        return "'@'"