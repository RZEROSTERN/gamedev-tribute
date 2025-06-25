import pygame
import gameconfig as gc

class Explosion(pygame.sprite.Sprite):
    def __init__(self, game, image_dictionary, image_type, power, group, row_number, column_number, size):
        super().__init__(group)
        self.game = game

        self.row_number = row_number
        self.column_number = column_number
        self.size = size

        self.y = (self.row_number * self.size) + gc.Y_OFFSET
        self.x = self.column_number * self.size

        self.index = 0
        self.animation_frame_rate = 75
        self.animation_timer = pygame.time.get_ticks()

        self.image_dictionary = image_dictionary
        self.image_type = image_type

        self.image = self.image_dictionary[self.image_type][self.index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        self.animate()

    def draw(self, window, x_offset):
        window.blit(self.image, (self.rect.x - x_offset, self.rect.y))

    def animate(self):
        if pygame.time.get_ticks() - self.animation_timer >= self.animation_frame_rate:
            self.index += 1
            if self.index == len(self.image_dictionary[self.image_type]):
                self.kill()
                return
            
            self.image = self.image_dictionary[self.image_type][self.index]
            self.animation_timer = pygame.time.get_ticks()