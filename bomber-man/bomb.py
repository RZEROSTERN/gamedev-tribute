import pygame
import gameconfig as gc

class Bomb(pygame.sprite.Sprite):
    def __init__(self, game, image_list, group, row_number, column_number, size):
        super().__init__(group)

        self.game = game
        self.row = row_number
        self.column = column_number

        self.size = size
        self.x = self.column * self.size
        self.y = (self.row * self.size) + gc.Y_OFFSET

        self.bomb_counter = 1
        self.bomb_timer = 12

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

    def draw(self, window, offset):
        window.blit(self.image, (self.rect.x - offset, self.rect.y))

    def insert_bomb_into_grid(self):
        self.game.level_matrix[self.row][self.column] = self

        for row in self.game.level_matrix:
            print(row)

    def animation(self):
        if pygame.time.get_ticks() - self.animation_timer >= self.animation_frame_time:
            self.image_index += 1
            self.image_index = self.image_index % self.animation_length
            self.image = self.image_list[self.image_index]
            self.animation_timer = pygame.time.get_ticks()

    def __repr__(self):
        return "'!'"

