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