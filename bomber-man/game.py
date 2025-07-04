import pygame
import gameconfig as gc
from enemy import Enemy
from character import Character
from blocks import HardBlock, SoftBlock
from random import choice, randint
from blocks import SpecialSoftBlock

class Game:
    def __init__(self, main, assets):
        self.main = main
        self.assets = assets

        self.camera_x_offset = 0

        self.groups = {
            "hard_blocks": pygame.sprite.Group(),
            "soft_blocks": pygame.sprite.Group(),
            "bomb": pygame.sprite.Group(),
            "player": pygame.sprite.Group(),
            "explosions": pygame.sprite.Group(),
            "enemies": pygame.sprite.Group(),
            "specials": pygame.sprite.Group(),
        }

        self.player = Character(self, self.assets.player_character, self.groups["player"], 3, 2, gc.TILE_SIZE)

        self.level = 1
        self.level_special = self.select_a_special()
        self.level_matrix = self.generate_level_matrix(gc.ROWS, gc.COLUMNS)

    def input(self):
        self.player.input()

    def update(self):
        for value in self.groups.values():
            for item in value:
                item.update()

        if self.groups["explosions"]:
            killed_enemies = pygame.sprite.groupcollide(self.groups["explosions"], self.groups["enemies"], False, False)

            if killed_enemies:
                for flame, enemies in killed_enemies.items():
                    for enemy in enemies:
                        if pygame.sprite.collide_mask(flame, enemy):
                            enemy.destroy()

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
        self.insert_power_up_into_matrix(level_matrix, self.level_special)
        self.insert_power_up_into_matrix(level_matrix, "exit")
        self.insert_enemies_into_level(level_matrix)

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
    
    def insert_power_up_into_matrix(self, matrix, special):
        power_up = special
        valid = False

        while not valid:
            row = randint(0, gc.ROWS)
            column = randint(0, gc.COLUMNS)

            if row == 0 or row == len(matrix) - 1 or column == 0 or column == len(matrix[0]) - 1:
                continue
            elif row % 2 == 0 and column % 2 == 0:
                continue
            elif row in [2, 3, 4] and column in [1, 2, 3]:
                continue
            elif matrix[row][column] != "_":
                continue
            else:
                valid = True
                
            cell = SpecialSoftBlock(self, self.assets.soft_block["soft_block"], self.groups["soft_blocks"], row, column, gc.TILE_SIZE, power_up)
            matrix[row][column] = cell
    
    def update_x_camera_offset_player_position(self, player_x_position):
        if player_x_position >= 576 and player_x_position <= 1280:
            self.camera_x_offset = player_x_position - 576

    def insert_enemies_into_level(self, matrix, enemies = None):
        enemies_list = self.select_enemies_to_spawn() if enemies is None else enemies

        player_column = self.player.column_number
        player_row = self.player.row_number

        for enemy in enemies_list:
            valid_choice = False

            while not valid_choice:
                row = randint(0, gc.ROWS)
                column = randint(0, gc.COLUMNS)

                if row in [player_row - 3, player_row - 2, player_row - 1, player_row, player_row + 1, player_row + 2, player_row + 3] and \
                   column in [player_column - 3, player_column - 2, player_column - 1, player_column, player_column + 1, player_column + 2, player_column + 3]:
                    continue
                elif matrix[row][column] == "_":
                    valid_choice = True
                    Enemy(self, self.assets.enemies[enemy], self.groups["enemies"], enemy, row, column, gc.TILE_SIZE)
                else:
                    continue

    def regenerate_stage(self):
        for key in self.groups.keys():
            if key == "player":
                continue
            self.groups[key].empty()

        self.level_matrix.clear()
        self.level_matrix = self.generate_level_matrix(gc.ROWS, gc.COLUMNS)

        self.camera_x_offset = 0

    def select_enemies_to_spawn(self):
        enemies_list = []
        enemies = {
            0: "ballom",
            1: "ballom",
            2: "onil",
            3: "dahl",
            4: "minvo",
            5: "doria",
            6: "ovape",
            7: "pass",
            8: "pontan",
        }

        if self.level <= 8:
            self.add_enemies_to_list(8, 2, 0, enemies, enemies_list)
        elif self.level <= 17:
            self.add_enemies_to_list(7, 2, 1, enemies, enemies_list)
        elif self.level <= 26:
            self.add_enemies_to_list(6, 3, 1, enemies, enemies_list)
        elif self.level <= 35:
            self.add_enemies_to_list(5, 3, 2, enemies, enemies_list)
        elif self.level <= 45:
            self.add_enemies_to_list(4, 4, 2, enemies, enemies_list)
        else:
            self.add_enemies_to_list(3, 4, 4, enemies, enemies_list)
        
        return enemies_list
    
    def add_enemies_to_list(self, num1, num2, num3, enemies, enemies_list):
        for num in range(num1):
            enemies_list.append("ballom")
        for num in range(num2):
            enemies_list.append(enemies[self.level % 9])
        for num in range(num3):
            enemies_list.append(choice(list(enemies.values())))

        return
    
    def select_a_special(self):
        specials = list(gc.SPECIALS.keys())
        specials.remove("exit")

        if self.level == 4:
            power_up = "speed_up"
        elif self.level == 1:
            power_up = "bomb_up"
        elif self.player.bombs_limit <= 2 or self.player.power <= 2:
            power_up = choice(["bomb_up", "power_up"])
        else:
            if self.player.wall_pass:
                specials.remove("wall_hack")
            if self.player.remote:
                specials.remove("remote")
            if self.player.bomb_pass:
                specials.remove("bomb_pass")
            if self.player.flame_pass:
                specials.remove("flame_pass")
            if self.player.bombs_limit == 10:
                specials.remove("bomb_up")
            if self.player.power == 10:
                specials.remove("fire_up")
            
            power_up = choice(specials)

        return power_up
    
    def new_stage(self):
        self.level += 1
        self.level_special = self.select_a_special()
        self.player.set_player_position()
        self.player.set_player_images()
        self.regenerate_stage()

        print(self.level)