import pygame
import gameconfig as gc
from scores import ScoreBanner

class Explosion(pygame.sprite.Sprite):
    def __init__(self, assets, group, position, explode_type = 1, score = 100):
        super().__init__()
        self.assets = assets
        self.groups = group
        self.explosion_group = self.groups["Explosion"]
        self.explosion_group.add(self)

        self.score = score

        self.position = position
        self.explode_type = explode_type
        self.frame_index = 1
        self.images = self.assets.explosions
        self.image = self.images["explode_1"]
        self.rect = self.image.get_rect(center = (self.position))

        self.animation_timer = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.animation_timer >= 100:
            self.frame_index += 1

            if self.frame_index >= len(self.images):
                self.kill()

                if self.score == 0:
                    return
                ScoreBanner(self.assets, self.groups, self.rect.center, self.score)
            if self.explode_type == 1 and self.frame_index > 3:
                self.kill()

            self.animation_timer = pygame.time.get_ticks()
            self.image = self.images[f"explode_{self.frame_index}"]
            self.rect = self.image.get_rect(center = self.position)

    def draw(self, window):
        window.blit(self.image, self.rect)