import pygame
import gameconfig as gc
from bomb import Bomb

class Character(pygame.sprite.Sprite):
    def __init__(self, game, image_dictionary, group, row_number, column_number, size):
        super().__init__(group)
        self.game = game

        self.row_number = row_number
        self.column_number = column_number
        self.size = size

        self.set_player(image_dictionary)

        self.lives = 3

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.main.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.main.run = False
                elif event.key == pygame.K_SPACE:
                    row, column = ((self.rect.centery - gc.Y_OFFSET) // gc.TILE_SIZE, self.rect.centerx // self.size)

                    if self.game.level_matrix[row][column] == "_" and self.bombs_planted < self.bombs_limit:
                        Bomb(self.game, self.game.assets.bomb["bomb"], self.game.groups["bomb"], self.power, row, column, gc.TILE_SIZE, self.remote)
                elif event.key == pygame.K_j and self.remote and self.game.groups["bomb"]:
                    bomb_list = self.game.groups["bomb"].sprites()
                    bomb_list[-1].explode()

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.move("walk_right")
        elif keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.move("walk_left")
        elif keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            self.move("walk_up")
        elif keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
            self.move("walk_down")

        self.rect.topleft = (self.x, self.y)

    def update(self):
        if not self.invincible:
            if len(self.game.groups["explosions"]) > 0 and not self.flame_pass:
                self.deadly_collisions(self.game.groups["explosions"])

            self.deadly_collisions(self.game.groups["enemies"])

        if self.action == "dead_animation":
            self.animate("dead_animation")

        if not self.invincible:
            return
        
        if pygame.time.get_ticks() - self.invincible_timer >= gc.INVINCIBLE_TIME:
            self.invincible = False

    def draw(self, window, offset):
        window.blit(self.image, (self.rect.x - offset, self.rect.y))
        pygame.draw.rect(window, gc.RED, (self.rect.x - offset, self.rect.y, 64, 64), 1)

    def animate(self, action):
        if pygame.time.get_ticks() - self.animation_time_set >= self.animation_time:
            self.index += 1

            if self.index == len(self.image_dictionary[action]):
                self.index = 0

                if self.action == "dead_animation":
                    self.reset_player()
                    return
                # self.index = self.index % len(self.image_dictionary[action])

            self.image = self.image_dictionary[action][self.index]
            self.animation_time_set = pygame.time.get_ticks()

    def move(self, action):
        if not self.alive:
            return
        
        if action != self.action:
            self.action = action
            self.index = 0
        
        direction = {"walk_left": -self.speed, "walk_right": self.speed, "walk_up": -self.speed, "walk_down": self.speed}

        if action == "walk_left" or action == "walk_right":
            self.x += direction[action]
        elif action == "walk_up" or action == "walk_down":
            self.y += direction[action]

        self.animate(action)
        
        self.snap_to_grid()
        self.play_area_restriction(64, (gc.COLUMNS - 1) * 64, gc.Y_OFFSET + 64, ((gc.ROWS - 1) * 64) + gc.Y_OFFSET)

        self.rect.topleft = (self.x, self.y)

        self.collision_detection_items(self.game.groups["hard_blocks"])

        if self.wall_pass:
            self.collision_detection_items(self.game.groups["soft_blocks"])
        
        self.collision_detection_items(self.game.groups["bomb"])

        self.game.update_x_camera_offset_player_position(self.rect.x)

    def collision_detection_items(self, item_list):
        for item in item_list:
            if self.rect.colliderect(item.rect) and item.passable == False:
                if self.action == "walk_left":
                    if self.rect.left < item.rect.right:
                        self.rect.left = item.rect.right
                        self.x, self.y = self.rect.topleft
                        return
                if self.action == "walk_right":
                    if self.rect.right > item.rect.left:
                        self.rect.right = item.rect.left
                        self.x, self.y = self.rect.topleft
                        return
                
                if self.action == "walk_up":
                    if self.rect.top < item.rect.bottom:
                        self.rect.top = item.rect.bottom
                        self.x, self.y = self.rect.topleft
                        return
                if self.action == "walk_down":
                    if self.rect.bottom > item.rect.top:
                        self.rect.bottom = item.rect.top
                        self.x, self.y = self.rect.topleft
                        return
                    
    def snap_to_grid(self):
        x_pos = self.x % gc.TILE_SIZE
        y_pos = (self.y - gc.Y_OFFSET) % gc.TILE_SIZE

        if self.action in ["walk_up", "walk_down"]:
            if x_pos <= 12:
                self.x = self.x - x_pos
            if x_pos >= 52:
                self.x = self.x + (gc.TILE_SIZE - x_pos)
        elif self.action in ["walk_left", "walk_right"]:
            if y_pos <= 12:
                self.y = self.y - y_pos
            if y_pos >= 52:
                self.y = self.y + (gc.TILE_SIZE - y_pos)

    def play_area_restriction(self, left_x, right_x, top_y, bottom_y):
        if self.x < left_x:
            self.x = left_x
        elif self.x > right_x:
            self.x = right_x

        if self.y < top_y:
            self.y = top_y
        elif self.y > bottom_y:
            self.y = bottom_y

    def set_player_position(self):
        self.x = self.column_number * self.size
        self.y = (self.row_number * self.size) + gc.Y_OFFSET

    def set_player_images(self):
        self.image = self.image_dictionary[self.action][self.index] #Definitive image. Still not implemented.
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def set_player(self, image_dictionary):
        self.set_player_position()

        self.alive = True
        self.speed = 3
        self.bombs_limit = 1
        self.remote = False  # Remote control for the last planted bomb
        self.power = 1
        self.bomb_pass = False
        self.flame_pass = False
        self.wall_pass = False
        self.invincible = False
        self.invincible_timer = None
        
        self.action = "walk_right"

        self.bombs_planted = 0

        self.index = 0
        self.animation_time = 50
        self.animation_time_set = pygame.time.get_ticks()
        self.image_dictionary = image_dictionary

        self.set_player_images()

    def reset_player(self):
        self.lives -= 1

        if self.lives < 0:
            self.game.main.run = False
            return
        
        self.game.regenerate_stage()
        self.set_player(self.image_dictionary)

    def deadly_collisions(self, group):
        if not self.alive:
            return
        
        for item in group:
            if not self.rect.colliderect(item.rect):
                continue
            if pygame.sprite.collide_mask(self, item):
                self.action = "dead_animation"
                self.alive = False
                return