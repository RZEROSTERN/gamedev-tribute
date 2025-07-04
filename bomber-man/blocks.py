import pygame
import gameconfig as gc
from specials import Special

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
                if self.image_index == len(self.image_list) - 1:
                    self.kill()
                
                self.image = self.image_list[self.image_index]
                self.animation_timer = pygame.time.get_ticks()

            for enemy in self.game.groups["enemies"]:
                if enemy.destroyed:
                    continue
                if not self.rect.colliderect(enemy):
                    continue
                if pygame.sprite.collide_mask(self, enemy):
                    enemy.destroy()

            if not self.rect.colliderect(self.game.player.rect):
                if pygame.sprite.collide_mask(self, self.game.player):
                    self.game.player.alive = False
                    self.game.player.action = "dead_animation"

    def destroy_soft_block(self):
        if not self.destroyed:
            self.animation_timer = pygame.time.get_ticks()
            self.destroyed = True
            self.game.level_matrix[self.row][self.column] = "_"

    def __repr__(self):
        return "'@'"
    
class SpecialSoftBlock(SoftBlock):
    def __init__(self, game, images, group, row_number, column_number, size, special_type):
        super().__init__(game, images, group, row_number, column_number, size)
        
        self.special_type = special_type
        print((self.row, self.column))

    def kill(self):
        print(f"Special block of type {self.special_type} at ({self.row}, {self.column}) destroyed.")
        super().kill()
        self.place_special_block()

    def place_special_block(self):
        special_cell = Special(self.game, self.game.assets.specials[self.special_type][0], self.special_type, self.game.groups["specials"], self.row, self.column, self.size)
        self.game.level_matrix[self.row][self.column] = special_cell

    def __repr__(self):
        return "'*'"