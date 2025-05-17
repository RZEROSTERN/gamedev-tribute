import pygame
import gameconfig as gc
from character import Character
from blocks import HardBlock, SoftBlock
from random import choice

class Game:
    def __init__(self, main, assets):
        self.main = main
        self.assets = assets

        self.camera_x_offset = 0

        self.groups = {
            "hard_blocks": pygame.sprite.Group(),
            "soft_blocks": pygame.sprite.Group(),
            "player": pygame.sprite.Group()
        }

        self.player = Character(self, self.assets.player_character, self.groups["player"], 3, 2, gc.TILE_SIZE)

        self.level = 1
        self.level_matrix = self.generate_level_matrix(gc.ROWS, gc.COLUMNS)

    def input(self):
        self.player.input()

    def update(self):
        for value in self.groups.values():
            for item in value:
                item.update()

    def draw(self, window):
        window.fill(gc.GREY)

        for row_number, row in enumerate(self.level_matrix):
            for column_number, col in enumerate(row):
                window.blit(self.assets.background["background"][0], ((column_number * gc.TILE_SIZE) - self.camera_x_offset, (row_number * gc.TILE_SIZE) + gc.Y_OFFSET))

        for value in self.groups.values():
            for item in value:
                item.draw(window, self.camera_x_offset)

    def generate_level_matrix(self, rows, columns):
        level_matrix = []

        for row in range(rows + 1):
            line = []

            for column in range(columns + 1):
                line.append("_")

            level_matrix.append(line)

        self.insert_hard_blocks_into_matrix(level_matrix)
        self.insert_soft_blocks_into_matrix(level_matrix)

        for row in level_matrix:
            print(row)

        return level_matrix
    
    def insert_hard_blocks_into_matrix(self, matrix):
        for row_number, row in enumerate(matrix):
            for column_number, col in enumerate(row):
                if row_number == 0 or row_number == len(matrix) - 1 or \
                    column_number == 0 or column_number == len(row) - 1 or \
                    (row_number % 2 == 0 and column_number % 2 == 0):
                    matrix[row_number][column_number] = HardBlock(self, self.assets.hard_block["hard_block"], self.groups["hard_blocks"], row_number, column_number, gc.TILE_SIZE)

        return
    
    def insert_soft_blocks_into_matrix(self, matrix):
        for row_number, row in enumerate(matrix):
            for column_number, col in enumerate(row):
                if row_number == 0 or row_number == len(matrix) - 1 or \
                    column_number == 0 or column_number == len(row) - 1 or \
                    (row_number % 2 == 0 and column_number % 2 == 0):
                    continue
                elif row_number in [2, 3, 4] and column_number in [1, 2, 3]:
                    continue
                else:
                    cell = choice(["@", "_", "_", "_"])

                    if cell == "@":
                        cell = SoftBlock(self, self.assets.soft_block["soft_block"], self.groups["soft_blocks"], row_number, column_number, gc.TILE_SIZE)
                        matrix[row_number][column_number] = cell

        return
    
    def update_x_camera_offset_player_position(self, player_x_position):
        if player_x_position >= 576 and player_x_position <= 1280:
            self.camera_x_offset = player_x_position - 576
