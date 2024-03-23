import pygame
import gameconfig as gc


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

        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()

    def draw(self, window):
        window.blit(self.image, self.rect)
        pygame.draw.rect(window, gc.GREEN, self.rect, 1)

    def move(self):
        speed = gc.TANK_SPEED * 3

        if self.direction == "Up":
            self.yPos -= speed
        elif self.direction == "Down":
            self.yPos += speed
        elif self.direction == "Left":
            self.xPos -= speed
        elif self.direction == "Right":
            self.xPos += speed

        self.rect.center = (self.xPos, self.yPos)

    def collide_edge_of_screen(self):
        if self.rect.top <= gc.SCREEN_BORDER_TOP or \
                self.rect.bottom >= gc.SCREEN_BORDER_BOTTOM or \
                self.rect.left <= gc.SCREEN_BORDER_LEFT or \
                self.rect.right >= gc.SCREEN_BORDER_RIGHT:
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

                    self.kill()
                    break

            if (self.owner.enemy == False and tank.enemy == True) or \
                    (self.owner.enemy == True and tank.enemy == False):
                if pygame.sprite.collide_mask(self, tank):
                    self.update_owner()
                    tank.destroy_tank()
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

    def update_owner(self):
        if self.owner.bullet_sum > 0:
            self.owner.bullet_sum -= 1
