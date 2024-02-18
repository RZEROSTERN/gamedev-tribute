SPRITE_SIZE = 16
SPRITE_SCALE = 4
IMAGE_SIZE = SPRITE_SIZE * SPRITE_SCALE

SCREEN_WIDTH = 16 * IMAGE_SIZE
SCREEN_HEIGHT = 14 * IMAGE_SIZE

FPS = 60

BLACK = (0,0,0)

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
    "shield": [(SPRITE_SIZE * SPRITE_SIZE), (16 * 7), 16, 16],
    "freeze": [(16 * 17), (16 * 7), 16, 16],
    "fortify": [(16 * 18), (16 * 7), 16, 16],
    "power": [(16 * 19), (16 * 7), 16, 16],
    "explosion": [(16 * 20), (16 * 7), 16, 16],
    "extra_life": [(16 * 21), (16 * 7), 16, 16],
    "special": [(16 * 22), (16 * 7), 16, 16]
}

SCORE = {
    "100": [((16 * 18), (16 * 10), 16, 16)],
    "200": [((16 * 19), (16 * 10), 16, 16)],
    "300": [((16 * 20), (16 * 10), 16, 16)],
    "400": [((16 * 21), (16 * 10), 16, 16)],
    "500": [((16 * 22), (16 * 10), 16, 16)],
}

# Aquí me quedé