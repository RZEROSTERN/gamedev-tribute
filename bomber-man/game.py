import pygame
import gameconfig as gc
from character import Character
from blocks import HardBlock

class Game:
    def __init__(self, main, assets):
        self.main = main
        self.assets = assets

        self.player = Character(self, self.assets.player_character)

        self.hard_blocks = pygame.sprite.Group()

        self.level = 1
        self.level_matrix = self.generate_level_matrix(gc.ROWS, gc.COLUMNS)

    def input(self):
        self.player.input()

    def update(self):
        self.hard_blocks.update()
        self.player.update()

    def draw(self, window):
        self.hard_blocks.draw(window)
        self.player.draw(window)

    def generate_level_matrix(self, rows, columns):
        level_matrix = []

        for row in range(rows + 1):
            line = []

            for column in range(columns + 1):
                line.append("_")

            level_matrix.append(line)

        self.insert_hard_blocks_into_matrix(level_matrix)

        for row in level_matrix:
            print(row)

        return level_matrix
    
    def insert_hard_blocks_into_matrix(self, matrix):
        for row_number, row in enumerate(matrix):
            for column_number, col in enumerate(row):
                if row_number == 0 or row_number == len(matrix) - 1 or \
                    column_number == 0 or column_number == len(row) - 1 or \
                    (row_number % 2 == 0 and column_number % 2 == 0):
                    matrix[row_number][column_number] = HardBlock(self, self.assets.hard_block["hard_block"], self.hard_blocks, row_number, column_number, gc.TILE_SIZE)

        return