import pygame
import gameconfig as gc
from fireball import Fireball

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

        self.power = power
        self.passable = False
        self.calculate_explosive_path()

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

    def calculate_explosive_path(self):
        valid_directions = [True, True, True, True]  # left, right, up, down

        for power_cell in range(self.power):
            directions = self.calculate_direction_cells(power_cell)

            for index, direction in enumerate(directions):
                if not valid_directions[index]:
                    continue

                if self.game.level_matrix[direction[0]][direction[1]] == "_":
                    if power_cell == self.power - 1:
                        Fireball(self.image_dictionary[direction[4]], self.game.groups["explosions"], direction[0], direction[1], gc.TILE_SIZE)
                    elif self.game.level_matrix[direction[2]][direction[3]] in self.game.groups["hard_blocks"].sprites():
                        Fireball(self.image_dictionary[direction[5]], self.game.groups["explosions"], direction[0], direction[1], gc.TILE_SIZE)
                        valid_directions[index] = False
                    else:
                        Fireball(self.image_dictionary[direction[5]], self.game.groups["explosions"], direction[0], direction[1], gc.TILE_SIZE)
                elif self.game.level_matrix[direction[0]][direction[1]] in self.game.groups["bomb"].sprites():
                    self.game.level_matrix[direction[0]][direction[1]].explode()
                    valid_directions[index] = False
                elif self.game.level_matrix[direction[0]][direction[1]] in self.game.groups["soft_blocks"].sprites():
                    self.game.level_matrix[direction[0]][direction[1]].destroy_soft_block()
                    valid_directions[index] = False
                elif self.game.level_matrix[direction[0]][direction[1]] in self.game.groups["specials"].sprites():
                    self.game.level_matrix[direction[0]][direction[1]].hit_by_explosion()
                    valid_directions[index] = False
                else:
                    valid_directions[index] = False
                    continue
            
    def calculate_direction_cells(self, cell):
        """Returns a list of the four cells in the up and down, left and right directions"""
        left = (self.row_number, self.column_number - (cell + 1),  # Check cell immediate left
                self.row_number, self.column_number - (cell + 2),  # Check cell left of that
                "left_end", "left_mid")
        right = (self.row_number, self.column_number + (cell + 1),  # Check cell immediate right
                self.row_number, self.column_number + (cell + 2),  # Check cell right of that
                "right_end", "right_mid")
        up = (self.row_number - (cell + 1), self.column_number,  # Check cell immediate up
              self.row_number - (cell + 2), self.column_number,  #  Check cell above that
              "up_end", "up_mid")
        down = (self.row_number + (cell + 1), self.column_number,  # Check cell immediate down
              self.row_number + (cell + 2), self.column_number,  # Check cell below that
              "down_end", "down_mid")
        return [left, right, up, down]
