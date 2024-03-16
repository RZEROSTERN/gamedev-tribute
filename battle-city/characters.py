import pygame
import gameconfig as gc

class Tank(pygame.sprite.Sprite):
    def __init__(self, game, assets, groups, position, direction, colour = "Silver", tank_level = 0):
        super().__init__()

        self.game = game
        self.assets = assets
        self.groups = groups

        self.tank_group = self.groups["All_Tanks"]
        
        self.tank_group.add(self)

        self.tank_images = self.assets.tank_images
        self.spawn_images = self.assets.spawn_star_images

        self.spawn_pos = position
        self.xPos, self.yPos = self.spawn_pos
        self.direction = direction

        self.spawning = True
        self.active = False

        self.tank_level = tank_level
        self.colour = colour
        self.tank_speed = gc.TANK_SPEED

        self.frame_index = 0
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]
        self.rect = self.image.get_rect(topleft = (self.spawn_pos))

        self.spawn_image = self.spawn_images[f"star_{self.frame_index}"]
        self.spawn_timer = pygame.time.get_ticks()
        self.spawn_anim_timer = pygame.time.get_ticks()

    def input(self):
        pass

    def update(self):
        if self.spawning:
            if pygame.time.get_ticks() - self.spawn_anim_timer >= 50:
                self.spawn_animation()
            if pygame.time.get_ticks() - self.spawn_timer > 1000:
                self.frame_index = 0
                self.spawning = False
                self.active = True

        return

    def draw(self, window):
        if self.spawning:
            window.blit(self.spawn_image, self.rect)

        if self.active:
            window.blit(self.image, self.rect)
            pygame.draw.rect(window, gc.RED, self.rect, 1)

    def move_tank(self, direction):
        if self.spawning:
            return
        
        self.direction = direction

        if direction == "Up":
            self.yPos -= self.tank_speed
        elif direction == "Down":
            self.yPos += self.tank_speed
        elif direction == "Left":
            self.xPos -= self.tank_speed
        elif direction == "Right":
            self.xPos += self.tank_speed

        self.rect.topleft = (self.xPos, self.yPos)
        self.tank_movement_animation()
        self.tank_on_tank_collisions()
        
    def tank_movement_animation(self):
        self.frame_index += 1
        imagelistlength = len(self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction])
        self.frame_index = self.frame_index % imagelistlength
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]

    def spawn_animation(self):
        self.frame_index += 1
        self.frame_index = self.frame_index % len(self.spawn_images)
        self.spawn_image = self.spawn_images[f"star_{self.frame_index}"]
        self.spawn_anim_timer = pygame.time.get_ticks()

    def tank_on_tank_collisions(self):
        tank_collision = pygame.sprite.spritecollide(self, self.tank_group, False)

        if len(tank_collision) == 1:
            return
        
        for tank in tank_collision:
            if tank == self:
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



class PlayerTank(Tank):
    def __init__(self, game, assets, groups, position, direction, colour, tank_level):
        super().__init__(game, assets, groups, position, direction, colour, tank_level)

    def input(self, keypressed):
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