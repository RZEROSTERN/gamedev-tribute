SPRITE_SIZE = 16
SPRITE_SCALE = 4
IMAGE_SIZE = SPRITE_SIZE * SPRITE_SCALE

SCREEN_WIDTH = 16 * IMAGE_SIZE
SCREEN_HEIGHT = 14 * IMAGE_SIZE

GAME_SCREEN = (IMAGE_SIZE, IMAGE_SIZE // 2, IMAGE_SIZE * 13, IMAGE_SIZE * 13)
INFO_PANEL_X, INFO_PANEL_Y = SCREEN_WIDTH - (IMAGE_SIZE * 2), IMAGE_SIZE // 2
STD_ENEMIES = 20

SCREEN_BORDER_LEFT = GAME_SCREEN[0]
SCREEN_BORDER_TOP = GAME_SCREEN[1]
SCREEN_BORDER_RIGHT = GAME_SCREEN[2] + SCREEN_BORDER_LEFT
SCREEN_BORDER_BOTTOM = GAME_SCREEN[3] + SCREEN_BORDER_TOP
SCREEN_SCROLL_SPEED = 5

FPS = 60

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (99, 99, 99)
GREEN = (0, 255, 0)

TANK_SPEED = IMAGE_SIZE // SPRITE_SIZE
TANK_PARALYSIS = 2000

SPAWN_STAR = {
    "star_0": [(SPRITE_SIZE * 16), (SPRITE_SIZE * 6), SPRITE_SIZE, SPRITE_SIZE], 
    "star_1": [(SPRITE_SIZE * 17), (SPRITE_SIZE * 6), SPRITE_SIZE, SPRITE_SIZE], 
    "star_2": [(SPRITE_SIZE * 18), (SPRITE_SIZE * 6), SPRITE_SIZE, SPRITE_SIZE], 
    "star_3": [(SPRITE_SIZE * 19), (SPRITE_SIZE * 6), SPRITE_SIZE, SPRITE_SIZE]
}

SHIELD = {
    "shield_1": [(SPRITE_SIZE * 16), (SPRITE_SIZE * 9), 16, 16],
    "shield_2": [(SPRITE_SIZE * 16), (SPRITE_SIZE * 9), 16, 16]
}

POWER_UPS = {
    "shield": [(16 * 16), (16 * 7), 16, 16],
    "freeze": [(16 * 17), (16 * 7), 16, 16],
    "fortify": [(16 * 18), (16 * 7), 16, 16],
    "power": [(16 * 19), (16 * 7), 16, 16],
    "explosion": [(16 * 20), (16 * 7), 16, 16],
    "extra_life": [(16 * 21), (16 * 7), 16, 16],
    "special": [(16 * 22), (16 * 7), 16, 16]
}

SCORE = {
    "100": [(SPRITE_SIZE * 18), (SPRITE_SIZE * 10), 16, 16],
    "200": [(SPRITE_SIZE * 19), (SPRITE_SIZE * 10), 16, 16],
    "300": [(SPRITE_SIZE * 20), (SPRITE_SIZE * 10), 16, 16],
    "400": [(SPRITE_SIZE * 21), (SPRITE_SIZE * 10), 16, 16],
    "500": [(SPRITE_SIZE * 22), (SPRITE_SIZE * 10), 16, 16]
}

FLAG = {
    "Phoenix_Alive": [(16 * 19), (16 * 2), 16, 16],
    "Phoenix_Destroyed": [(16 * 20), (16 * 2), 16, 16]
}

EXPLOSIONS = {
    "explode_1": [(SPRITE_SIZE * 16), (SPRITE_SIZE * 8), 16, 16],
    "explode_2": [(SPRITE_SIZE * 17), (SPRITE_SIZE * 8), 16, 16],
    "explode_3": [(SPRITE_SIZE * 18), (SPRITE_SIZE * 8), 16, 16],
    "explode_4": [(SPRITE_SIZE * 19), (SPRITE_SIZE * 8), 32, 32],
    "explode_5": [(SPRITE_SIZE * 20), (SPRITE_SIZE * 8), 32, 32]
}

BULLETS = {
    "Up": [(SPRITE_SIZE * 20), (SPRITE_SIZE * 6) + 4, 8, 8],
    "Left": [(SPRITE_SIZE * 20) + 8, (SPRITE_SIZE * 6) + 4, 8, 8],
    "Down": [(SPRITE_SIZE * 21), (SPRITE_SIZE * 6) + 4, 8, 8],
    "Right": [(SPRITE_SIZE * 21) + 8, (SPRITE_SIZE * 6) + 4, 8, 8],
}

MAP_TILES = {
    # Brick
    432: {
        "small": [SPRITE_SIZE * 16, SPRITE_SIZE * 4, 8, 8],
        "small_right": [(SPRITE_SIZE * 16) + 12, SPRITE_SIZE * 4, 4, 8],
        "small_bot": [SPRITE_SIZE * 17, (SPRITE_SIZE * 4) + 4, 8, 4],
        "small_left": [(SPRITE_SIZE * 17) + 8, SPRITE_SIZE * 4, 4, 8],
        "small_top": [(SPRITE_SIZE * 18), SPRITE_SIZE * 4, 8, 4],
    },
    # Steel
    482: {
        "small": [SPRITE_SIZE * 16, (SPRITE_SIZE * 4) + 8, 8, 8]
    },
    # Forest
    483: {
        "small": [(SPRITE_SIZE * 16) + 8, (SPRITE_SIZE * 4) + 8, 8, 8]
    },
    # Ice
    484: {
        "small": [(SPRITE_SIZE * 17), (SPRITE_SIZE * 4) + 8, 8, 8]
    },
    # Water
    533: {
        "small_1": [(SPRITE_SIZE * 16) + 8, (SPRITE_SIZE * 5), 8, 8],
        "small_2": [(SPRITE_SIZE * 17), (SPRITE_SIZE * 5), 8, 8],
    }
}

HUD_INFO = {
    "stage": [(16 * 20) + 8, (16 * 11), 40, 8],
    "num_0": [(16 * 20) + 8, (16 * 11) + 8, 8, 8],
    "num_1": [(16 * 21), (16 * 11) + 8, 8, 8],
    "num_2": [(16 * 21) + 8, (16 * 11) + 8, 8, 8],
    "num_3": [(16 * 22), (16 * 11) + 8, 8, 8],
    "num_4": [(16 * 22) + 8, (16 * 11) + 8, 8, 8],
    "num_5": [(16 * 20) + 8, (16 * 12), 8, 8],
    "num_6": [(16 * 21), (16 * 12), 8, 8],
    "num_7": [(16 * 21) + 8, (16 * 12), 8, 8],
    "num_8": [(16 * 22), (16 * 12), 8, 8],
    "num_9": [(16 * 22) + 8, (16 * 12), 8, 8],
    "life": [(16 * 20), (16 * 12), 8, 8],
    "info_panel": [(16 * 23), (16 * 0), 32, (16 * 15)],
    "grey_square": [(16 * 23), (16 * 0), 8, 8],
}

NUMS = {
    0: [0,0,8,8], 1: [8,0,8,8], 2: [16,0,8,8], 3: [24,0,8,8], 4: [32, 0, 8, 8],
    5: [0,8,8,8], 6: [8,8,8,8], 7: [16,8,8,8], 8: [24,8,8,8], 9: [32, 8, 8, 8]
}

CONTEXT = {
    "pause": [(16 * 18), (16 * 11), 40, 8],
    "game_over": [(16 * 18), (16 * 11) + 8, 32, 16]
}

ENEMY_TANK_SPAWNS = [(0, 0), (0, 1), (1, 0), (1, 1),
                     (12, 0), (12, 1), (13, 0), (13, 1),
                     (24, 0), (24, 1), (25, 0), (25, 1)]

PLAYER_TANK_SPAWNS = [(8, 24), (8, 25), (9, 24), (9, 25),
                      (16, 24), (16, 25), (17, 24), (17, 25)]

BASE = [(12, 24), (12, 25), (13,24), (13,25)]

FORT = [(11, 25), (11, 24), (11, 23), (12, 23), (13, 23), (14, 23), (14, 24), (14, 25)]
