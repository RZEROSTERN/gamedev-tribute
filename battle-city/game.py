import random
import pygame
import gameconfig as gc
from characters import PlayerTank, Tank
from gamehud import GameHud


class Game:
    def __init__(self, main, assets, player1=True, player2=False):
        self.main = main
        self.assets = assets

        self.groups = {
            "All_Tanks": pygame.sprite.Group(),
            "Bullets": pygame.sprite.Group()
        }

        self.player1_active = player1
        self.player2_active = player2

        self.hud = GameHud(self, self.assets)

        self.level_num = 1
        self.data = self.main.levels

        if self.player1_active:
            self.player1 = PlayerTank(self, self.assets, self.groups, gc.P1_POS, "Up", "Gold", 0)

        if self.player2_active:
            self.player2 = PlayerTank(self, self.assets, self.groups, gc.P2_POS, "Up", "Green", 1)

        self.enemies = gc.STD_ENEMIES

        self.create_new_stage()

        self.end_game = False

    def input(self):
        keypressed = pygame.key.get_pressed()

        if self.player1_active:
            self.player1.input(keypressed)

        if self.player2_active:
            self.player2.input(keypressed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.end_game = True

                if event.key == pygame.K_SPACE:
                    if self.player1_active:
                        self.player1.shoot()

                if event.key == pygame.K_RCTRL:
                    if self.player2_active:
                        self.player2.shoot()

                if event.key == pygame.K_RETURN:
                    Tank(self, self.assets, self.groups, (400, 400), "Down")
                    self.enemies -= 1

    def update(self):
        self.hud.update()

        # if self.player1_active:
        #    self.player1.update()

        # if self.player2_active:
        #    self.player2.update()

        for dictKey in self.groups.keys():
            for item in self.groups[dictKey]:
                item.update()

    def draw(self, window):
        self.hud.draw(window)

        # if self.player1_active:
        #    self.player1.draw(window)

        # if self.player2_active:
        #    self.player2.draw(window)

        for dictKey in self.groups.keys():
            for item in self.groups[dictKey]:
                item.draw(window)

    def create_new_stage(self):
        self.current_level_data = self.data.level_data[self.level_num - 1]

        self.enemies = random.choice([16, 17, 18, 19, 20])
        self.enemies = 5

        self.enemies_killed = self.enemies

        self.load_level_data(self.current_level_data)

        self.generate_spawn_queue()
        self.spawn_pos_index = 0
        self.spawn_queue_index = 0

        if self.player1_active:
            self.player1.new_stage_spawn(gc.P1_POS)

    def load_level_data(self, level):
        self.grid = []

        for i, row in enumerate(level):
            line = []
            for j, tile in enumerate(row):
                pos = (gc.SCREEN_BORDER_LEFT + (j * gc.IMAGE_SIZE // 2), gc.SCREEN_BORDER_TOP + (i * gc.IMAGE_SIZE // 2))

                # IMPROVE THIS SHIT !!!
                if int(tile) < 0:
                    line.append(" ")
                elif int(tile) == 432:
                    line.append(f"{tile}")
                elif int(tile) == 482:
                    line.append(f"{tile}")
                elif int(tile) == 483:
                    line.append(f"{tile}")
                elif int(tile) == 484:
                    line.append(f"{tile}")
                elif int(tile) == 533:
                    line.append(f"{tile}")
                else:
                    line.append(f"{tile}")

            self.grid.append(line)

        for row in self.grid:
            print(row)

    def generate_spawn_queue(self):
        self.spawn_queue_ratios = gc.TANK_SPAWN_QUEUE[f"queue_{str((self.level_num % 36) // 3)}"]
        self.spawn_queue = []

        for lvl, ratio in enumerate(self.spawn_queue_ratios):
            for i in range(int(round(self.enemies * (ratio / 100)))):
                self.spawn_queue.append(f"level_{lvl}")

        random.shuffle(self.spawn_queue)
