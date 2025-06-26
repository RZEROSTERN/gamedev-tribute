import pygame
import gameconfig as gc


class Fireball(pygame.sprite.Sprite):
    def __init__(self, image_list, group, row_number, column_number, size):
        super().__init__(group)
        self.row_number = row_number
        self.column_number = column_number
        self.size = size

        self.x = self.column_number * self.size
        self.y = (self.row_number * self.size) + gc.Y_OFFSET

        self.index = 0
        self.animation_frame_rate = 75
        self.animation_timer = pygame.time.get_ticks()
        self.image_list = image_list
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.passable = False

    def update(self):
        self.animate()

    def draw(self, window, x_offset):
        window.blit(self.image, (self.rect.x - x_offset, self.rect.y))

    def animate(self):
        if pygame.time.get_ticks() - self.animation_timer >= self.animation_frame_rate:
            self.index += 1
            if self.index == len(self.image_list):
                self.kill()
                return
            
            self.image = self.image_list[self.index]
            self.animation_timer = pygame.time.get_ticks()