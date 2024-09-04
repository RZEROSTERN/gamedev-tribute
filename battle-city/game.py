import random
import pygame
import gameconfig as gc
from characters import PlayerTank, Tank, EnemyTank, SpecialTank
from gamehud import GameHud
from tile import BrickTile, SteelTile, ForestTile, IceTile, WaterTile
from fadeanimate import Fade
from scorescreen import ScoreScreen

class Game:
    def __init__(self, main, assets, player1=True, player2=False):
        self.main = main
        self.assets = assets

        self.groups = {
            "Ice_Tiles": pygame.sprite.Group(),
            "Water_Tiles": pygame.sprite.Group(),
            "Player_Tanks": pygame.sprite.Group(),
            "All_Tanks": pygame.sprite.Group(),
            "Bullets": pygame.sprite.Group(),
            "Destructable_Tiles": pygame.sprite.Group(),
            "Impassable_Tiles": pygame.sprite.Group(),
            "Forest_Tiles": pygame.sprite.Group(),
            "Power_Ups": pygame.sprite.Group(),
        }

        self.top_score = 20000
        self.player1_active = player1
        self.player1_score = 0
        self.player2_active = player2
        self.player2_score = 0

        self.hud = GameHud(self, self.assets)

        self.level_num = 1
        self.level_complete = False
        self.level_transition_timer = None
        self.data = self.main.levels

        self.fade = Fade(self, self.assets, 10)
        self.score_screen = ScoreScreen(self, self.assets)

        if self.player1_active:
            self.player1 = PlayerTank(self, self.assets, self.groups, gc.P1_POS, "Up", "Gold", 0)

        if self.player2_active:
            self.player2 = PlayerTank(self, self.assets, self.groups, gc.P2_POS, "Up", "Green", 1)

        self.enemies = gc.STD_ENEMIES
        self.enemy_tank_spawn_timer = gc.TANK_SPAWNING_TIME
        self.enemy_spawn_positions = [gc.COM1_POSITION, gc.COM2_POSITION, gc.COM3_POSITION]

        self.create_new_stage()
        self.fortify = False
        self.fortify_timer = pygame.time.get_ticks()

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

        if self.fade.fade_active:
            self.fade.update()

            if not self.fade.fade_active:
                for tank in self.groups["All_Tanks"]:
                    tank.spawn_timer = pygame.time.get_ticks()
            
            return
        
        if self.fortify:
            if pygame.time.get_ticks() - self.fortify_timer > 10000:
                self.power_up_fortify(start = False, end = True)
                self.fortify = False

        # if self.player1_active:
        #    self.player1.update()

        # if self.player2_active:
        #    self.player2.update()

        for dictKey in self.groups.keys():
            if dictKey == "Impassable_Tiles":
                continue
            for item in self.groups[dictKey]:
                item.update()

        self.spawn_enemy_tanks()

        if self.enemies_killed <= 0 and self.level_complete == False:
            self.level_complete = True
            self.level_transition_timer = pygame.time.get_ticks()
        
        if self.level_complete:
            if pygame.time.get_ticks() - self.level_transition_timer >= gc.TRANSITION_TIMER:
                self.stage_transition()

    def draw(self, window):
        self.hud.draw(window)

        if self.score_screen.active:
            self.score_screen.draw(window)
            return

        # if self.player1_active:
        #    self.player1.draw(window)

        # if self.player2_active:
        #    self.player2.draw(window)

        for dictKey in self.groups.keys():
            if dictKey == "Player_Tanks":
                continue

            if self.fade.fade_active == True and (dictKey == "All_Tanks" or dictKey == "Player_Tanks"):
                continue

            for item in self.groups[dictKey]:
                item.draw(window)

        if self.fade.fade_active:
            self.fade.draw(window)

    def create_new_stage(self):
        for key, value in self.groups.items():
            if key == "Player_Tanks":
                continue
            value.empty()

        self.current_level_data = self.data.level_data[self.level_num - 1]

        self.enemies = random.choice([16, 17, 18, 19, 20])
        # self.enemies = 10

        self.enemies_killed = self.enemies

        self.load_level_data(self.current_level_data)
        self.level_complete = False
        
        self.fade.level = self.level_num
        self.fade.stage_image = self.fade.create_stage_image()
        self.fade.fade_active = True

        self.generate_spawn_queue()
        self.spawn_pos_index = 0
        self.spawn_queue_index = 0

        if self.player1_active:
            self.player1.new_stage_spawn(gc.P1_POS)
        if self.player2_active:
            self.player2.new_stage_spawn(gc.P2_POS)

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
                    map_tile = BrickTile(pos, self.groups["Destructable_Tiles"], self.assets.brick_tiles)
                    self.groups["Impassable_Tiles"].add(map_tile)
                elif int(tile) == 482:
                    line.append(f"{tile}")
                    map_tile = SteelTile(pos, self.groups["Destructable_Tiles"], self.assets.steel_tiles)
                    self.groups["Impassable_Tiles"].add(map_tile)
                elif int(tile) == 483:
                    line.append(f"{tile}")
                    map_tile = ForestTile(pos, self.groups["Forest_Tiles"], self.assets.forest_tiles)
                elif int(tile) == 484:
                    line.append(f"{tile}")
                    map_tile = IceTile(pos, self.groups["Ice_Tiles"], self.assets.ice_tiles)
                elif int(tile) == 533:
                    line.append(f"{tile}")
                    map_tile = WaterTile(pos, self.groups["Water_Tiles"], self.assets.water_tiles)
                    self.groups["Impassable_Tiles"].add(map_tile)
                else:
                    line.append(f"{tile}")

            self.grid.append(line)

        #for row in self.grid:
        #    print(row)

    def generate_spawn_queue(self):
        self.spawn_queue_ratios = gc.TANK_SPAWN_QUEUE[f"queue_{str((self.level_num % 36) // 3)}"]
        self.spawn_queue = []

        for lvl, ratio in enumerate(self.spawn_queue_ratios):
            for i in range(int(round(self.enemies * (ratio / 100)))):
                self.spawn_queue.append(f"level_{lvl}")

        random.shuffle(self.spawn_queue)

    def spawn_enemy_tanks(self):
        if self.enemies == 0:
            return
        
        if pygame.time.get_ticks() - self.enemy_tank_spawn_timer >= gc.TANK_SPAWNING_TIME:
            position = self.enemy_spawn_positions[self.spawn_pos_index % 3]
            tank_level = gc.TANK_CRITERIA[self.spawn_queue[self.spawn_queue_index % len(self.spawn_queue)]]["image"]

            special_tank = random.randint(1, len(self.spawn_queue))

            if special_tank == self.spawn_queue_index:
                SpecialTank(self, self.assets, self.groups, position, "Down", "Silver", tank_level)
            else:
                EnemyTank(self, self.assets, self.groups, position, "Down", "Silver", tank_level)

            self.enemy_tank_spawn_timer = pygame.time.get_ticks()
            self.spawn_pos_index += 1
            self.spawn_queue_index += 1
            self.enemies -= 1

    def stage_transition(self):
        if not self.score_screen.active:
            self.score_screen.timer = pygame.time.get_ticks()

            if self.player1_active:
                self.score_screen.p1_score = self.player1_score
                self.score_screen.p1_kill_list = sorted(self.player1.score_list)

            if self.player2_active:
                self.score_screen.p1_score = self.player2_score
                self.score_screen.p2_kill_list = sorted(self.player2.score_list)

            self.score_screen.update_basic_info(self.top_score, self.level_num) 

        self.score_screen.active = True
        self.score_screen.update()

    def change_level(self, p1_score, p2_score):
        self.level_num += 1
        self.level_num = self.level_num % len(self.data.level_data)
        self.player1_score = p1_score
        self.player2_score = p2_score
        self.create_new_stage()

    def power_up_fortify(self, start = True, end = False):
        off_x, off_y = gc.SCREEN_BORDER_LEFT, gc.SCREEN_BORDER_TOP

        positions = [
            (off_x + gc.IMAGE_SIZE // 2 * 11, off_y + gc.IMAGE_SIZE // 2 * 25),
            (off_x + gc.IMAGE_SIZE // 2 * 11, off_y + gc.IMAGE_SIZE // 2 * 24),
            (off_x + gc.IMAGE_SIZE // 2 * 11, off_y + gc.IMAGE_SIZE // 2 * 23),
            (off_x + gc.IMAGE_SIZE // 2 * 12, off_y + gc.IMAGE_SIZE // 2 * 23),
            (off_x + gc.IMAGE_SIZE // 2 * 13, off_y + gc.IMAGE_SIZE // 2 * 23),
            (off_x + gc.IMAGE_SIZE // 2 * 14, off_y + gc.IMAGE_SIZE // 2 * 23),
            (off_x + gc.IMAGE_SIZE // 2 * 14, off_y + gc.IMAGE_SIZE // 2 * 24),
            (off_x + gc.IMAGE_SIZE // 2 * 14, off_y + gc.IMAGE_SIZE // 2 * 25),
        ]

        if start:
            for pos in positions:
                pos_rect = pygame.rect.Rect(pos[0], pos[1], gc.IMAGE_SIZE // 2, gc.IMAGE_SIZE // 2)

                for rectangle in self.groups["Impassable_Tiles"]:
                    if rectangle.rect.colliderect(pos_rect):
                        rectangle.kill()

                map_tile = SteelTile(pos, self.groups["Destructable_Tiles"], self.assets.steel_tiles)
                self.groups["Impassable_Tiles"].add(map_tile)
        elif end:
            for pos in positions:
                pos_rect = pygame.rect.Rect(pos[0], pos[1], gc.IMAGE_SIZE // 2, gc.IMAGE_SIZE // 2)

                for rectangle in self.groups["Impassable_Tiles"]:
                    if rectangle.rect.colliderect(pos_rect):
                        rectangle.kill()

                map_tile = BrickTile(pos, self.groups["Destructable_Tiles"], self.assets.brick_tiles)
                self.groups["Impassable_Tiles"].add(map_tile)