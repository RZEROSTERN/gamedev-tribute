import pygame
import gameconfig as gc
from random import choice

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, image_dictionary, group, type, row_number, column_number, size):
        super().__init__(group)
        self.game = game

        self.type = type
        self.row = row_number
        self.column = column_number
        self.size = size
        self.x = self.column * self.size
        self.y = (self.row * self.size) + gc.Y_OFFSET

        self.speed = gc.ENEMIES[self.type]["speed"]
        self.wall_hack = gc.ENEMIES[self.type]["wall_hack"]
        self.chase_player = gc.ENEMIES[self.type]["chase_player"]
        self.line_of_sight = gc.ENEMIES[self.type]["line_of_sight"] * self.size
        self.see_player_hack = gc.ENEMIES[self.type]["see_player_hack"]

        self.destroyed = False
        self.direction = "left"
        self.direction_movement = {
            "left":  -self.speed,
            "right": self.speed,
            "up": -self.speed,
            "down": self.speed
        }
        self.change_direction_timer = pygame.time.get_ticks()
        self.direction_time = 1500

        self.index = 0
        self.action = f"walk_{self.direction}"
        self.image_dictionary = image_dictionary
        self.animation_frame_rate = 100
        self.animation_timer = pygame.time.get_ticks()

        self.image = self.image_dictionary[self.action][self.index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.start_position = self.rect.center
        self.end_position = self.game.player.rect.center


    def update(self):
        self.movement()
        self.update_line_of_sight_with_player()
        self.animate()

    def draw(self, window, x_offset):
        window.blit(self.image, (self.rect.x - x_offset, self.rect.y))
        pygame.draw.line(window, "black", (self.start_position[0] - x_offset, self.start_position[1]), (self.end_position[0] - x_offset, self.end_position[1]), 2)

    def movement(self):
        if self.destroyed:
            return
        
        move_direction = self.action.split("_")[1]
        
        if move_direction in ["left", "right"]:
            self.x += self.direction_movement[move_direction]
        else:
            self.y += self.direction_movement[move_direction]

        directions = ["left", "right", "up", "down"]

        self.new_direction(self.game.groups["hard_blocks"], move_direction, directions)

        if not self.wall_hack:
            self.new_direction(self.game.groups["soft_blocks"], move_direction, directions)
        
        self.new_direction(self.game.groups["bomb"], move_direction, directions)

        if self.chase_player:
            if self.check_line_of_sight_distance():
                pass
            elif self.intersecting_items_with_line_of_sight("hard_blocks"):
                pass
            elif self.intersecting_items_with_line_of_sight("soft_blocks") and self.see_player_hack:
                pass
            elif self.intersecting_items_with_line_of_sight("bomb") and not self.see_player_hack:
                pass
            else:
                self.chase_the_player()
            
        self.change_directions(directions)

        self.rect.update(self.x, self.y, self.size, self.size)

    def collision_detection_blocks(self, group, move_direction):
        for block in group:
            if block.rect.colliderect(self.rect):
                if move_direction == "left" and self.rect.right > block.rect.right:
                    self.x = block.rect.right
                    return move_direction
                if move_direction == "right" and self.rect.left < block.rect.left:
                    self.x = block.rect.left - self.size
                    return move_direction
                if move_direction == "up" and self.rect.bottom > block.rect.bottom:
                    self.y = block.rect.bottom
                    return move_direction
                if move_direction == "down" and self.rect.top < block.rect.top:
                    self.y = block.rect.top - self.size
                    return move_direction
        
        return None
    
    def new_direction(self, group, move_direction, directions):
        direction = self.collision_detection_blocks(group, move_direction)

        if direction:
            directions.remove(direction)
            new_direction = choice(directions)
            self.action = f"walk_{new_direction}"
            self.change_direction_timer = pygame.time.get_ticks()

    def change_directions(self, direction_list):
        if pygame.time.get_ticks() - self.change_direction_timer < self.direction_time:
            return
        
        if self.x % self.size != 0 or (self.y - gc.Y_OFFSET) % self.size != 0:
            return
        
        row = int((self.y - gc.Y_OFFSET) // self.size)
        column = int(self.x // self.size)

        if row % 2 == 0 and column % 2 == 0:
            return
        
        if not self.wall_hack:
            self.determine_if_direction_valid(direction_list, row, column)

        new_direction = choice(direction_list)
        self.action = f"walk_{new_direction}"

        self.change_direction_timer = pygame.time.get_ticks()
        return
        

    def determine_if_direction_valid(self, direction_list, row, column):
        if self.game.level_matrix[row - 1][column] != "_":
            direction_list.remove("up")
        if self.game.level_matrix[row + 1][column] != "_":
            direction_list.remove("down")
        if self.game.level_matrix[row][column - 1] != "_":
            direction_list.remove("left")
        if self.game.level_matrix[row][column + 1] != "_":
            direction_list.remove("right")

        if len(direction_list) == 0:
            direction_list.append("left")
        return
    
    def animate(self):
        if pygame.time.get_ticks() - self.animation_timer >= self.animation_frame_rate:
            self.index += 1

            if self.destroyed and self.index == len(self.image_dictionary[self.action]):
                self.kill()
            
            self.index = self.index % len(self.image_dictionary[self.action])
            self.image = self.image_dictionary[self.action][self.index]
            self.animation_timer = pygame.time.get_ticks()
    
    def destroy(self):
        self.destroyed = True
        self.index = 0
        self.action = "death"
        self.image = self.image_dictionary[self.action][self.index]

    def update_line_of_sight_with_player(self):
        self.start_position = self.rect.center
        self.end_position = self.game.player.rect.center

    def chase_the_player(self):
        enemy_column = self.start_position[0] // self.size
        enemy_row = self.start_position[1] // self.size
        player_column = self.end_position[0] // self.size
        player_row = self.end_position[1] // self.size

        if enemy_column > player_column and ((self.y - gc.Y_OFFSET) % self.size) + 32 == self.size // 2:
            self.action = "walk_left"
        elif enemy_column < player_column and ((self.y - gc.Y_OFFSET) % self.size) + 32 == self.size // 2:
            self.action = "walk_right"
        elif enemy_row > player_row and (self.x % self.size) + 32 == self.size // 2:
            self.action = "walk_down"
        elif enemy_row < player_row and (self.x % self.size) + 32 == self.size // 2:
            self.action = "walk_up"

        self.change_direction_timer = pygame.time.get_ticks()

    def check_line_of_sight_distance(self):
        x_distance = abs(self.end_position[0] - self.start_position[0])
        y_distance = abs(self.end_position[1] - self.start_position[1])

        if x_distance > self.line_of_sight or y_distance > self.line_of_sight:
            return True
        
        return False
    
    def intersecting_items_with_line_of_sight(self, group):
        for item in self.game.groups[group]:
            if item.rect.clipline(self.start_position, self.end_position):
                return True
            
        return False