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
        self.spawn_pos = position
        self.xPos, self.yPos = self.spawn_pos
        self.direction = direction

        self.active = True
        self.tank_level = tank_level
        self.colour = colour
        self.tank_speed = gc.TANK_SPEED

        self.frame_index = 0
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]
        self.rect = self.image.get_rect(topleft = (self.spawn_pos))

    def input(self):
        pass

    def update(self):
        pass

    def draw(self, window):
        if self.active:
            window.blit(self.image, self.rect)

    def move_tank(self, direction):
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
        
    def tank_movement_animation(self):
        self.frame_index += 1
        imagelistlength = len(self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction])
        self.frame_index = self.frame_index % imagelistlength
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]

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