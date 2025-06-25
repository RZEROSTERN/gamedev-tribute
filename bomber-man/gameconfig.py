SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 892

FPS = 60

Y_OFFSET = 92

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
    "walk_left": [(0,1), (0,0), (0,2)],
    "walk_down": [(0,4), (0,3), (0,5)],
    "walk_right": [(0,7), (0,6), (0,8)],
    "walk_up": [(0,10), (0,9), (0,11)],
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
    "down_end": [(4, 0), (4, 1), (4, 2), (4, 3)],
    "left_mid": [(3, 4), (3, 5), (3, 6), (3, 7)],
    "right_mid": [(3, 4), (3, 5), (3, 6), (3, 7)],
    "up_mid": [(4, 4), (4, 5), (4, 6), (4, 7)],
    "down_mid": [(4, 4), (4, 5), (4, 6), (4, 7)],
}
