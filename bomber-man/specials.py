import pygame
import gameconfig as gc

class Special(pygame.sprite.Sprite):
    def __init__(self, game, image, name, group, row_number, column_number, size):
        super().__init__(group)
        
        self.game = game
        self.name = name

        self.row = row_number
        self.column = column_number
        self.size = size
        self.x = self.column * self.size
        self.y = (self.row * self.size) + gc.Y_OFFSET

        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.power_up_activate = {
            "bomb_up": self.bomb_up_special,
            "fire_up": self.fire_up_special,
            "speed_up": self.speed_up_special,
            "wall_pass": self.wall_pass_special,
            "remote": self.remote_special,
            "bomb_pass": self.bomb_pass_special,
            "flame_pass": self.flame_pass_special,
            "invincible": self.invincible_special,
            "exit": self.end_stage,
        }

    def update(self):
        if self.game.player.rect.collidepoint(self.rect.center):
            self.power_up_activate[self.name](self.game.player)

            if self.name == "exit":
                return

            self.game.level_matrix[self.row][self.column] = "_"
            self.kill()
            return

    def draw(self, window, x_offset):
        window.blit(self.image, (self.rect.x - x_offset, self.rect.y))

    def bomb_up_special(self, player):
        player.bombs_limit += 1
        
    def fire_up_special(self, player):
        player.power += 1

    def speed_up_special(self, player):
        player.speed += 1

    def wall_pass_special(self, player):
        player.wall_pass = True

    def remote_special(self, player):
        player.remote = True

    def bomb_pass_special(self, player):
        player.bomb_pass = True

    def flame_pass_special(self, player):
        player.flame_pass = True

    def invincible_special(self, player):
        player.invicible = True
        player.invincible_timer = pygame.time.get_ticks()

    def end_stage(self, player):
        if len(self.game.groups["enemies"].sprites()) > 0:
            return
        
        self.game.new_stage()

    def hit_by_explosion(self):        
        enemies = []

        for _ in range(10):
            enemies.append(gc.SPECIAL_CONNECTIONS[self.name])

        self.game.insert_enemies_into_level(self.game.level_matrix, enemies)

    def __repr__(self):
        return "'*'"
    
