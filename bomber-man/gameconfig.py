SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 892

FPS = 60

Y_OFFSET = 92

ENEMIES = {
    "ballom": {"speed": 1, "wall_hack": False, "chase_player": False, "line_of_sight": 0, "see_player_hack": False},
    "onil": {"speed": 2, "wall_hack": False, "chase_player": True, "line_of_sight": 4, "see_player_hack": False},
    "dahl": {"speed": 2, "wall_hack": False, "chase_player": False, "line_of_sight": 0, "see_player_hack": False},
    "minvo": {"speed": 2, "wall_hack": True, "chase_player": True, "line_of_sight": 4, "see_player_hack": True},
    "doria": {"speed": 0.5, "wall_hack": True, "chase_player": True, "line_of_sight": 6, "see_player_hack": True},
    "ovape": {"speed": 1, "wall_hack": True, "chase_player": True, "line_of_sight": 8, "see_player_hack": False},
    "pass": {"speed": 2, "wall_hack": True, "chase_player": True, "line_of_sight": 12, "see_player_hack": False},
    "pontan": {"speed": 4, "wall_hack": True, "chase_player": True, "line_of_sight": 30, "see_player_hack": False},
}

GAME_TITLE = "Bomberman"

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (188, 188, 188)

SPRITESHEET_PATH = "assets"
SPRITESHEET_NAME = "spritesheet.png"
SPRITESHEET_WIDTH = 192 * 4
SPRITESHEET_HEIGHT = 272 * 4

TILE_SIZE = 64
ROWS = 12
COLUMNS = 30

# Sprite sheet coordinates

PLAYER = { 
    "walk_left": [(0,0), (0,1), (0,2)],
    "walk_down": [(0,3), (0,4), (0,5)],
    "walk_right": [(0,6), (0,7), (0,8)],
    "walk_up": [(0,9), (0,10), (0,11)],
    "dead_animation": [(1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6)],
}

HARD_BLOCK = { "hard_block": [(1, 10)] }
SOFT_BLOCK = { "soft_block": [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)] }
BACKGROUND = { "background": [(2, 11)] }
BOMB = { "bomb": [(1,7), (1,8), (1,9), (1,8)] }

EXPLOSIONS = {
    "center": [(2, 7), (2, 8), (2, 9), (2, 10)],
    "left_end": [(3, 0), (3, 1), (3, 2), (3, 3)],
    "right_end": [(3, 0), (3, 1), (3, 2), (3, 3)],
    "up_end": [(4, 0), (4, 1), (4, 2), (4, 3)],
    "down_end":[(4, 0), (4, 1), (4, 2), (4, 3)],
    "left_mid": [(3, 4), (3, 5), (3, 6), (3, 7)],
    "right_mid": [(3, 4), (3, 5), (3, 6), (3, 7)],
    "up_mid": [(4, 4), (4, 5), (4, 6), (4, 7)],
    "down_mid": [(4, 4), (4, 5), (4, 6), (4, 7)]
}

BALLOM = {
    "walk_right": [(5, 0), (5, 1), (5, 2)],
    "walk_down": [(5, 0), (5, 1), (5, 2)],
    "walk_left": [(5, 3), (5, 4), (5, 5)],
    "walk_up": [(5, 3), (5, 4), (5, 5)],
    "death": [(5, 6), (5, 7), (5, 8), (5, 9), (5, 10)],
}

ONIL = {
    "walk_right": [(8, 0), (8, 1), (8, 2)],
    "walk_down": [(8, 0), (8, 1), (8, 2)],
    "walk_left": [(8, 3), (8, 4), (8, 5)],
    "walk_up": [(8, 3), (8, 4), (8, 5)],
    "death": [(8, 6), (8, 7), (8, 8), (8, 9), (8, 10)],
}

DAHL = {
    "walk_right": [(10, 0), (10, 1), (10, 2)],
    "walk_down": [(10, 0), (10, 1), (10, 2)],
    "walk_left": [(10, 3), (10, 4), (10, 5)],
    "walk_up": [(10, 3), (10, 4), (10, 5)],
    "death": [(10, 6), (10, 7), (10, 8), (10, 9), (10, 10)],
}

MINVO = {
    "walk_right": [(6, 0), (6, 1), (6, 2)],
    "walk_down": [(6, 0), (6, 1), (6, 2)],
    "walk_left": [(6, 3), (6, 4), (6, 5)],
    "walk_up": [(6, 3), (6, 4), (6, 5)],
    "death": [(6, 6), (6, 7), (6, 8), (6, 9), (6, 10)],
}

DORIA = {
    "walk_right": [(9, 0), (9, 1), (9, 2)],
    "walk_down": [(9, 0), (9, 1), (9, 2)],
    "walk_left": [(9, 3), (9, 4), (9, 5)],
    "walk_up": [(9, 3), (9, 4), (9, 5)],
    "death": [(9, 6), (9, 7), (9, 8), (9, 9), (9, 10)],
}

OVAPE = {
    "walk_right": [(11, 0), (11, 1), (11, 2)],
    "walk_down": [(11, 0), (11, 1), (11, 2)],
    "walk_left": [(11, 3), (11, 4), (11, 5)],
    "walk_up": [(11, 3), (11, 4), (11, 5)],
    "death": [(11, 6), (11, 7), (11, 8), (11, 9), (11, 10)],
}

PASS = {
    "walk_right": [(7, 0), (7, 1), (7, 2)],
    "walk_down": [(7, 0), (7, 1), (7, 2)],
    "walk_left": [(7, 3), (7, 4), (7, 5)],
    "walk_up": [(7, 3), (7, 4), (7, 5)],
    "death": [(7, 6), (7, 7), (7, 8), (7, 9), (7, 10)],
}

PONTAN = {
    "walk_right": [(5, 11), (6, 11), (7, 11), (8, 11)],
    "walk_down": [(5, 11), (6, 11), (7, 11), (8, 11)],
    "walk_left": [(5, 11), (6, 11), (7, 11), (8, 11)],
    "walk_up": [(5, 11), (6, 11), (7, 11), (8, 11)],
    "death": [(9, 11), (5, 7), (5, 8), (5, 9), (5, 10)],
}