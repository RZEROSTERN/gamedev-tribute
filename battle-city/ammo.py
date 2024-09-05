import pygame
import gameconfig as gc
from explosions import Explosion

class Bullet(pygame.sprite.Sprite):
    def __init__(self, groups, owner, pos, dir, assets):
        super().__init__()
        self.assets = assets
        self.group = groups

        self.tanks = self.group["All_Tanks"]
        self.bullet_group = self.group["Bullets"]

        self.xPos, self.yPos = pos
        self.direction = dir

        self.owner = owner
        self.power = self.owner.power
        self.speed = self.owner.bullet_speed

        self.images = self.assets.bullet_images
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect(center=(self.xPos, self.yPos))

        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()

        self.bullet_group.add(self)

    def update(self):
        self.move()
        self.collide_edge_of_screen()
        self.collide_with_tank()
        self.collision_with_bullet()
        self.collision_with_obstacle()
        self.base_collision()

        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()

    def draw(self, window):
        window.blit(self.image, self.rect)

    def move(self):
        if self.direction == "Up":
            self.yPos -= self.speed
        elif self.direction == "Down":
            self.yPos += self.speed
        elif self.direction == "Left":
            self.xPos -= self.speed
        elif self.direction == "Right":
            self.xPos += self.speed

        self.rect.center = (self.xPos, self.yPos)

    def collide_edge_of_screen(self):
        if self.rect.top <= gc.SCREEN_BORDER_TOP or \
                self.rect.bottom >= gc.SCREEN_BORDER_BOTTOM or \
                self.rect.left <= gc.SCREEN_BORDER_LEFT or \
                self.rect.right >= gc.SCREEN_BORDER_RIGHT:
            
            Explosion(self.assets, self.group, self.rect.center, 1)
            self.assets.channel_steel_sound.play(self.assets.steel_sound)
            self.update_owner()
            self.kill()

    def collide_with_tank(self):
        tank_collisions = pygame.sprite.spritecollide(self, self.tanks, False)

        for tank in tank_collisions:
            if self.owner == tank or tank.spawning == True:
                continue

            if self.owner.enemy == False and tank.enemy == False:
                if pygame.sprite.collide_mask(self, tank):
                    self.update_owner()
                    tank.paralyze_tank(gc.TANK_PARALYSIS)
                    Explosion(self.assets, self.group, self.rect.center, 1)
                    self.kill()
                    break

            if (self.owner.enemy == False and tank.enemy == True) or \
                    (self.owner.enemy == True and tank.enemy == False):
                if pygame.sprite.collide_mask(self, tank):
                    self.update_owner()
                    if not self.owner.enemy:
                        self.owner.score_list.append(gc.TANK_CRITERIA[tank.level]["score"])
                        
                    tank.destroy_tank()
                    Explosion(self.assets, self.group, self.rect.center, 1)
                    self.kill()
                    break

    def collision_with_bullet(self):
        bullet_hit = pygame.sprite.spritecollide(self, self.bullet_group, False)

        if len(bullet_hit) == 1:
            return

        for bullet in bullet_hit:
            if bullet == self:
                continue
            if pygame.sprite.collide_mask(self, bullet):
                bullet.update_owner()
                bullet.kill()
                self.update_owner()
                self.kill()
                break

    def collision_with_obstacle(self):
        obstacle_collide = pygame.sprite.spritecollide(self, self.group["Destructable_Tiles"], False)
        
        for obstacle in obstacle_collide:
            if obstacle.name == "Brick":
                self.assets.channel_brick_sound.play(self.assets.brick_sound)
            elif obstacle.name == "Steel":
                self.assets.channel_steel_sound.play(self.assets.steel_sound)

            obstacle.hit_by_bullet(self)
            Explosion(self.assets, self.group, self.rect.center, 1)
        
        # self.kill()

    def base_collision(self):
        if self.rect.colliderect(self.group["Eagle"].sprite.rect):
            Explosion(self.assets, self.group, self.rect.center, 1)
            self.update_owner()
            self.group["Eagle"].sprite.destroy_base()
            self.kill()

    def update_owner(self):
        if self.owner.bullet_sum > 0:
            self.owner.bullet_sum -= 1
