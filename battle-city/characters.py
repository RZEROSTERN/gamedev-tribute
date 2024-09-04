import random
import pygame
from ammo import Bullet
import gameconfig as gc
from powerups import PowerUps

class MyRect(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = None
        self.rect = pygame.Rect(x, y, width, height)



class Tank(pygame.sprite.Sprite):
    def __init__(self, game, assets, groups, position, direction, enemy=True, colour="Silver", tank_level=0):
        super().__init__()

        self.game = game
        self.assets = assets
        self.groups = groups

        self.tank_group = self.groups["All_Tanks"]
        self.player_group = self.groups["Player_Tanks"]

        self.tank_group.add(self)

        levels = {0: None, 1: None, 4: "level_0", 5: "level_1", 6: "level_2", 7: "level_3"}

        self.level = levels[tank_level]

        self.tank_images = self.assets.tank_images
        self.spawn_images = self.assets.spawn_star_images

        self.spawn_pos = position
        self.xPos, self.yPos = self.spawn_pos
        self.direction = direction

        self.spawning = True
        self.active = False
        self.amphibious = False

        self.tank_level = tank_level
        self.colour = colour
        self.tank_speed = gc.TANK_SPEED if not self.level else gc.TANK_SPEED * gc.TANK_CRITERIA[self.level]["speed"]
        self.power = 1 if not self.level else gc.TANK_CRITERIA[self.level]["power"]
        self.bullet_speed_modifier = 1
        self.bullet_speed = gc.TANK_SPEED * (3 * self.bullet_speed_modifier)
        self.score = 100 if not self.level else gc.TANK_CRITERIA[self.level]["score"]
        self.enemy = enemy
        self.tank_health = 1 if not self.level else gc.TANK_CRITERIA[self.level]["health"]

        self.frame_index = 0
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]
        self.rect = self.image.get_rect(topleft=(self.spawn_pos))
        self.width, self.height = self.image.get_size()

        self.bullet_limit = 1
        self.bullet_sum = 0
        self.shot_cooldown_time = 1000
        self.shot_cooldown = pygame.time.get_ticks()

        self.paralyzed = False
        self.paralysis = gc.TANK_PARALYSIS
        self.paralysis_timer = pygame.time.get_ticks()

        self.spawn_image = self.spawn_images[f"star_{self.frame_index}"]
        self.spawn_timer = pygame.time.get_ticks()
        self.spawn_anim_timer = pygame.time.get_ticks()

        self.mask_dict = self.get_various_masks()
        self.mask = self.mask_dict[self.direction]
        self.mask_image = self.mask.to_surface()
        self.mask_direction = self.direction

    def input(self):
        pass

    def update(self):
        self.mask_dict = self.get_various_masks()
        self.mask = self.mask_dict[self.direction]
        self.mask_image = self.mask.to_surface()
        self.mask_direction = self.direction

        if self.spawning:
            if pygame.time.get_ticks() - self.spawn_anim_timer >= 50:
                self.spawn_animation()
            if pygame.time.get_ticks() - self.spawn_timer > 2000:
                colliding_sprites = pygame.sprite.spritecollide(self, self.tank_group, False)

                if len(colliding_sprites) == 1:
                    self.frame_index = 0
                    self.spawning = False
                    self.active = True
                else:
                    self.spawn_star_collision(colliding_sprites)
            return

        if self.paralyzed:
            if pygame.time.get_ticks() - self.paralysis_timer >= self.paralysis:
                self.paralyzed = False

    def draw(self, window):
        if self.spawning:
            window.blit(self.spawn_image, self.rect)

        if self.active:
            window.blit(self.image, self.rect)
            pygame.draw.rect(window, gc.RED, self.rect, 1)

    def grid_alignment_movement(self, pos):
        if pos % (gc.IMAGE_SIZE // 2) != 0:
            if pos % (gc.IMAGE_SIZE // 2) < gc.IMAGE_SIZE // 4:
                pos -= (pos % (gc.IMAGE_SIZE // 4))
            elif pos % (gc.IMAGE_SIZE // 2) > gc.IMAGE_SIZE // 4:
                pos += (gc.IMAGE_SIZE // 4) - (pos % (gc.IMAGE_SIZE // 4))
            else:
                return pos
        return pos

    def move_tank(self, direction):
        if self.spawning:
            return

        self.direction = direction

        if self.paralyzed:
            self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]
            return

        if direction == "Up":
            self.yPos -= self.tank_speed
            self.xPos = self.grid_alignment_movement(self.xPos)
            if self.yPos < gc.SCREEN_BORDER_TOP:
                self.yPos = gc.SCREEN_BORDER_TOP

        elif direction == "Down":
            self.yPos += self.tank_speed
            self.xPos = self.grid_alignment_movement(self.xPos)
            if self.yPos + self.height > gc.SCREEN_BORDER_BOTTOM:
                self.yPos = gc.SCREEN_BORDER_BOTTOM - self.height

        elif direction == "Left":
            self.xPos -= self.tank_speed
            self.yPos = self.grid_alignment_movement(self.yPos)
            if self.xPos < gc.SCREEN_BORDER_LEFT:
                self.xPos = gc.SCREEN_BORDER_LEFT
        elif direction == "Right":
            self.xPos += self.tank_speed
            self.yPos = self.grid_alignment_movement(self.yPos)
            if self.xPos + self.width > gc.SCREEN_BORDER_RIGHT:
                self.xPos = gc.SCREEN_BORDER_RIGHT - self.width

        self.rect.topleft = (self.xPos, self.yPos)
        self.tank_movement_animation()
        self.tank_on_tank_collisions()
        self.tank_collision_with_obstacles()

    def tank_movement_animation(self):
        self.frame_index += 1
        imagelistlength = len(self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction])
        self.frame_index = self.frame_index % imagelistlength
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]

        if self.mask_direction != self.direction:
            self.mask_direction = self.direction
            self.mask = self.mask_dict[self.mask_direction]

    def spawn_animation(self):
        self.frame_index += 1
        self.frame_index = self.frame_index % len(self.spawn_images)
        self.spawn_image = self.spawn_images[f"star_{self.frame_index}"]
        self.spawn_anim_timer = pygame.time.get_ticks()

    def get_various_masks(self):
        images = {}

        for direction in ["Up", "Down", "Left", "Right"]:
            image_to_mask = self.tank_images[f"Tank_{self.tank_level}"][self.colour][direction][0]
            images.setdefault(direction, pygame.mask.from_surface(image_to_mask))

        return images

    def tank_on_tank_collisions(self):
        tank_collision = pygame.sprite.spritecollide(self, self.tank_group, False)

        if len(tank_collision) == 1:
            return

        for tank in tank_collision:
            if tank == self or tank.spawning == True:
                continue

            if self.direction == "Right":
                if self.rect.right >= tank.rect.left and \
                        self.rect.bottom > tank.rect.top and self.rect.top < tank.rect.bottom:
                    self.rect.right = tank.rect.left
                    self.xPos = self.rect.x
            elif self.direction == "Left":
                if self.rect.left <= tank.rect.right and \
                        self.rect.bottom > tank.rect.top and self.rect.top < tank.rect.bottom:
                    self.rect.left = tank.rect.right
                    self.xPos = self.rect.x
            elif self.direction == "Up":
                if self.rect.top <= tank.rect.bottom and \
                        self.rect.left < tank.rect.right and self.rect.right > tank.rect.left:
                    self.rect.top = tank.rect.bottom
                    self.yPos = self.rect.y
            elif self.direction == "Down":
                if self.rect.bottom >= tank.rect.top and \
                        self.rect.left < tank.rect.right and self.rect.right > tank.rect.left:
                    self.rect.bottom = tank.rect.top
                    self.yPos = self.rect.y

    def tank_collision_with_obstacles(self):
        wall_collision = pygame.sprite.spritecollide(self, self.groups["Impassable_Tiles"], False)
        
        for obstacle in wall_collision:
            if obstacle in self.groups["Water_Tiles"] and self.amphibious == True:
                continue

            if self.direction == "Right":
                if self.rect.right >= obstacle.rect.left:
                    self.rect.right = obstacle.rect.left
                    self.xPos = self.rect.x
            elif self.direction == "Left":
                if self.rect.left <= obstacle.rect.right:
                    self.rect.left = obstacle.rect.right
                    self.xPos = self.rect.x
            elif self.direction == "Down":
                if self.rect.bottom >= obstacle.rect.top:
                    self.rect.bottom = obstacle.rect.top
                    self.yPos = self.rect.y
            elif self.direction == "Up":
                if self.rect.top <= obstacle.rect.bottom:
                    self.rect.top = obstacle.rect.bottom
                    self.yPos = self.rect.y

    def spawn_star_collision(self, colliding_sprites):
        for tank in colliding_sprites:
            if tank.active:
                return
            
        for tank in colliding_sprites:
            if tank == self:
                continue
            if self.spawning and tank.spawning:
                self.frame_index = 0
                self.spawning = False
                self.active = True


    def shoot(self):
        if self.bullet_sum >= self.bullet_limit:
            return

        bullet = Bullet(self.groups, self, self.rect.center, self.direction, self.assets)
        self.bullet_sum += 1

    def paralyze_tank(self, paralysis_time):
        self.paralysis = paralysis_time
        self.paralyzed = True
        self.paralysis_timer = pygame.time.get_ticks()

    def destroy_tank(self):
        self.tank_health -= 1

        if self.tank_health <= 0:
            self.kill()
            self.game.enemies_killed -= 1
            return
        
        if self.tank_health == 3:
            self.colour = "Green"
        elif self.tank_health == 2:
            self.colour = "Gold"
        elif self.tank_health == 1:
            self.colour = "Silver"


class PlayerTank(Tank):
    def __init__(self, game, assets, groups, position, direction, colour, tank_level):
        super().__init__(game, assets, groups, position, direction, False, colour, tank_level)
        self.player_group.add(self)
        self.lives = 3
        
        self.dead = False
        self.game_over = False

        self.score_list = []

        self.shield_start = True
        self.shield = False
        self.shield_time_limit = 5000
        self.shield_timer = pygame.time.get_ticks()
        self.shield_images = self.assets.shield_images
        self.shield_img_index = 0
        self.shield_animation_timer = pygame.time.get_ticks()
        self.shield_image = self.shield_images[f"shield_{self.shield_img_index + 1}"]
        self.shield_image_rect = self.shield_image.get_rect(topleft = (self.rect.topleft))

    def input(self, keypressed):
        if self.game_over or self.dead:
            return
        
        if self.colour == "Gold":
            if keypressed[pygame.K_w]:
                self.move_tank("Up")
            elif keypressed[pygame.K_s]:
                self.move_tank("Down")
            elif keypressed[pygame.K_a]:
                self.move_tank("Left")
            elif keypressed[pygame.K_d]:
                self.move_tank("Right")

        if self.colour == "Green":
            if keypressed[pygame.K_UP]:
                self.move_tank("Up")
            elif keypressed[pygame.K_DOWN]:
                self.move_tank("Down")
            elif keypressed[pygame.K_LEFT]:
                self.move_tank("Left")
            elif keypressed[pygame.K_RIGHT]:
                self.move_tank("Right")

    def update(self):
        if self.game_over:
            return
        
        if not self.spawning:
            if self.shield_start:
                self.shield_timer = pygame.time.get_ticks()
                self.shield_start = False
                self.shield = True

            if self.shield:
                if pygame.time.get_ticks() - self.shield_animation_timer >= 50:
                    self.shield_img_index += 1
                    self.shield_animation_timer = pygame.time.get_ticks()

                self.shield_img_index = self.shield_img_index % 2
                self.shield_image = self.shield_images[f"shield_{self.shield_img_index + 1}"]

                self.shield_image_rect.topleft = self.rect.topleft

                if pygame.time.get_ticks() - self.shield_time_limit >= self.shield_timer:
                    self.shield = False
        
        super().update()

    def draw(self, window):
        if self.game_over:
            return
        
        super().draw(window)

        if self.shield and not self.spawning:
            window.blit(self.shield_image, self.shield_image_rect)

    def shoot(self):
        if self.game_over:
            return
        
        super().shoot()

    def destroy_tank(self):
        if self.shield:
            return
        
        if self.dead or self.game_over:
            return
        
        if self.tank_health > 1:
            self.tank_health = 1
            self.tank_level = 0
            self.power = 1
            self.amphibious = False
            self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]
            self.rect = self.image.get_rect(topleft = (self.xPos, self.yPos))
            self.mask_dict = self.get_various_masks()
            self.mask = self.mask_dict[self.direction]
            return
        
        self.dead = True
        self.lives -= 1

        if self.lives <= 0:
            self.game_over = True

        self.respawn_tank()

    def new_stage_spawn(self, spawn_pos):
        self.tank_group.add(self)
        self.spawning = True
        self.active = False
        self.shield_start = True
        self.direction =  "Up"
        self.xPos, self.yPos = spawn_pos
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]
        self.rect.topleft = (self.xPos, self.yPos)
        self.score_list.clear()

    def respawn_tank(self):
        self.spawning = True
        self.active = False
        self.spawn_timer = pygame.time.get_ticks()
        self.shield_start = True
        self.direction = "Up"
        self.tank_level = 0
        self.power = 1
        self.amphibious = False
        self.bullet_speed_modifier = 1
        self.bullet_limit = 1
        self.bullet_speed = gc.TANK_SPEED * (3 * self.bullet_speed_modifier)
        self.xPos, self.yPos = self.spawn_pos
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]
        self.rect = self.image.get_rect(topleft=(self.spawn_pos))
        self.mask_dict = self.get_various_masks()
        self.mask = self.mask_dict[self.direction]
        self.dead = False

class EnemyTank(Tank):
    def __init__(self, game, assets, groups, position, direction, colour, tank_level):
        super().__init__(game, assets, groups, position, direction, True, colour, tank_level)

        self.time_between_shots = random.choice([300, 600, 900])
        self.shot_timer = pygame.time.get_ticks()

        self.direction_rect = {
            "Left": MyRect(self.xPos - (self.width // 2), self.yPos, self.width // 2, self.height),
            "Right": MyRect(self.xPos + self.width, self.yPos, self.width // 2, self.height),
            "Up": MyRect(self.xPos, self.yPos - (self.height // 2), self.width, self.height // 2),
            "Down": MyRect(self.xPos, self.yPos + self.height, self.width, self.height // 2)
        }

        self.move_directions = []
        self.change_direction_timer = pygame.time.get_ticks()
        self.game_screen_rect = MyRect(gc.GAME_SCREEN[0], gc.GAME_SCREEN[1], gc.GAME_SCREEN[2], gc.GAME_SCREEN[3])

    def ai_shooting(self):
        if self.paralyzed:
            return
        if self.bullet_sum < self.bullet_limit:
            if pygame.time.get_ticks() - self.shot_timer >= self.time_between_shots:
                self.shoot()
                self.shot_timer = pygame.time.get_ticks()

    def ai_move(self, direction):
        super().move_tank(direction)

        self.direction_rect["Left"].rect.update(self.xPos - (self.width // 2), self.yPos, self.width // 2, self.height)
        self.direction_rect["Right"].rect.update(self.xPos + self.width, self.yPos, self.width // 2, self.height)
        self.direction_rect["Up"].rect.update(self.xPos, self.yPos - (self.height // 2), self.width, self.height // 2)
        self.direction_rect["Down"].rect.update(self.xPos, self.yPos + self.height, self.width, self.height // 2)

    def ai_move_direction(self):
        directional_list_copy = self.move_directions.copy()

        if pygame.time.get_ticks() - self.change_direction_timer <= 750:
            return
        
        for key, value in self.direction_rect.items():
            if pygame.Rect.contains(self.game_screen_rect.rect, value):
                obstacle = pygame.sprite.spritecollideany(value, self.groups["Impassable_Tiles"])

                if not obstacle:
                    if key not in directional_list_copy:
                        directional_list_copy.append(key)
                elif obstacle:
                    if value.rect.contains(obstacle.rect) and key in directional_list_copy:
                        directional_list_copy.remove(key)
                    else:
                        if key in directional_list_copy and key != self.direction:
                            directional_list_copy.remove(key)

                tank = pygame.sprite.spritecollideany(value, self.groups["All_Tanks"])

                if tank:
                    if key in directional_list_copy:
                        directional_list_copy.remove(key)
            else:
                if key in directional_list_copy:
                    directional_list_copy.remove(key)

        if self.move_directions != directional_list_copy or (self.direction not in directional_list_copy):
            self.move_directions = directional_list_copy.copy()

            if len(self.move_directions) > 0:
                self.direction = random.choice(self.move_directions)
            self.change_direction_timer = pygame.time.get_ticks()

    def update(self):
        super().update()

        if self.spawning:
            return
        
        self.ai_move(self.direction)
        self.ai_move_direction()
        self.ai_shooting()

    def draw(self, window):
        super().draw(window)

        for value in self.direction_rect.values():
            pygame.draw.rect(window, gc.GREEN, value.rect, 2)

class SpecialTank(EnemyTank):
    def __init__(self, game, assets, groups, position, direction, colour, tank_level):
        super().__init__(game, assets, groups, position, direction, colour, tank_level)

        self.colour_swap_timer = pygame.time.get_ticks()
        self.special = True

    def update(self):
        super().update()

        if self.special:
            if pygame.time.get_ticks() - self.colour_swap_timer >= 100:
                self.colour = "Special" if self.colour == "Silver" else "Silver"
                self.colour_swap_timer = pygame.time.get_ticks()

    def destroy_tank(self):
        if self.special:
            self.special = False
            PowerUps(self.game, self.assets, self.groups)

        super().destroy_tank()