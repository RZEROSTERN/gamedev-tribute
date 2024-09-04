import pygame
import random
import gameconfig as gc

class PowerUps(pygame.sprite.Sprite):
    def __init__(self, game, assets, groups):
        super().__init__()

        self.game = game
        self.assets = assets
        self.powerup_images = self.assets.power_up_images

        self.groups = groups
        self.groups["Power_Ups"].add(self)

        #self.power_up = self.randomly_select_power_up()
        self.power_up = "shield"
        self.power_up_timer = pygame.time.get_ticks()

        self.xPos = random.randint(gc.SCREEN_BORDER_LEFT, gc.SCREEN_BORDER_RIGHT - gc.IMAGE_SIZE)
        self.yPos = random.randint(gc.SCREEN_BORDER_TOP, gc.SCREEN_BORDER_BOTTOM - gc.IMAGE_SIZE)

        self.image = self.powerup_images[self.power_up]
        self.rect = self.image.get_rect(topleft = (self.xPos, self.yPos))

    def randomly_select_power_up(self):
        powerups = list(gc.POWER_UPS.keys())
        selected_power_up = random.choice(powerups)

        return selected_power_up
    
    def power_up_collected(self):
        self.kill()

    def shield(self, player):
        player.shield_start = True
    
    def update(self):
        if pygame.time.get_ticks() - self.power_up_timer >= 5000:
            self.kill()

        player_tank = pygame.sprite.spritecollideany(self, self.groups["Player_Tanks"])

        if player_tank:
            if self.power_up == "shield":
                self.shield(player_tank)
            
            self.power_up_collected()

    def draw(self, window):
        window.blit(self.image, self.rect)