import pygame, random
from assets.spaceship import Spaceship
from assets.shield import Shield
from assets.shield import grid
from assets.alien import Alien
from assets.alien import MisteryShip
from assets.laser import Laser

class Game:
    def __init__(self, screen_width, screen_height, offset):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.offset = offset
        self.spaceship_group.add(Spaceship(self.screen_width, self.screen_height, self.offset))
        self.shields = self.create_shields()
        self.aliens_group = pygame.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1
        self.alien_lasers_group = pygame.sprite.Group()
        self.mistery_ship_group = pygame.sprite.GroupSingle()
        self.lives = 3
        self.run = True
        self.score = 0
        self.highscore = 0
        self.load_high_score()
        self.explosion = pygame.mixer.Sound("assets/sounds/invaderkilled.wav")
        self.mistery_explosion = pygame.mixer.Sound("assets/sounds/ufo_highpitch.wav")

    def create_shields(self):
        shield_width = len(grid[0]) * 3
        gap =((self.screen_width + self.offset) - (4 * shield_width)) / 5
        shields = []

        for i in range(4):
            offset_x = (i+1) * gap + i * shield_width
            shield = Shield(offset_x, self.screen_height - 100)
            shields.append(shield)
        return shields
    
    def create_aliens(self):
        for row in range(5):
            for col in range(11):
                x = 75 + col * 55
                y = 110 + row * 55

                if row == 0:
                    alien_type = 3
                elif row in (1,2):
                    alien_type = 2
                else:
                    alien_type = 1

                alien = Alien(alien_type, x + (self.offset / 2), y)
                self.aliens_group.add(alien)

    def move_aliens(self):
        self.aliens_group.update(self.aliens_direction)

        alien_sprites = self.aliens_group.sprites()

        for alien in alien_sprites:
            if alien.rect.right >= self.screen_width + (self.offset / 2):
                self.aliens_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= self.offset / 2:
                self.aliens_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance

    def alien_shoot_laser(self):
        if self.aliens_group.sprites():
            random_alien = random.choice(self.aliens_group.sprites())
            laser_sprite = Laser(random_alien.rect.center, -6, self.screen_height)

            self.alien_lasers_group.add(laser_sprite)

    def create_mistery_ship(self):
        mistery_ship = MisteryShip(self.screen_width, self.offset)
        self.mistery_ship_group.add(mistery_ship)
        mistery_ship.mistery_ship_sound.play()

    def check_for_collisions(self):
        # Spaceship
        if self.spaceship_group.sprite.lasers_group:
            for laser_sprite in self.spaceship_group.sprite.lasers_group:
                aliens_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_group, True)
                
                if aliens_hit:
                    self.explosion.play()
                    for alien in aliens_hit:
                        self.score += alien.type * 100
                        self.check_for_high_score()
                        laser_sprite.kill()

                if pygame.sprite.spritecollide(laser_sprite, self.mistery_ship_group, True):
                    self.score += 500
                    self.mistery_explosion.play()
                    self.check_for_high_score()
                    laser_sprite.kill()

                for shield in self.shields:
                    if pygame.sprite.spritecollide(laser_sprite, shield.blocks_group, True):
                        laser_sprite.kill()

        # Aliens lasers
        if self.alien_lasers_group:
            for laser_sprite in self.alien_lasers_group:
                if pygame.sprite.spritecollide(laser_sprite, self.spaceship_group, False):
                    laser_sprite.kill()
                    self.lives -= 1

                    if self.lives == 0:
                        self.game_over()
                    

                for shield in self.shields:
                    if pygame.sprite.spritecollide(laser_sprite, shield.blocks_group, True):
                        laser_sprite.kill()

        if self.aliens_group:
            for alien in self.aliens_group:
                for shield in self.shields:
                    pygame.sprite.spritecollide(alien, shield.blocks_group, True)

                if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
                    print("Spaceship HIT with ALIEN")

    def game_over(self):
        self.run = False

    def reset(self):
        self.run = True
        self.lives = 3
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.create_aliens()
        self.mistery_ship_group.empty()
        self.shields = self.create_shields()
        self.score = 0
                
    def check_for_high_score(self):
        if self.score > self.highscore:
            self.highscore = self.score

            with open("highscore.txt", "w") as file:
                file.write(str(self.highscore))

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as file:
                self.highscore = int(file.read())
        except FileNotFoundError:
            self.highscore = 0