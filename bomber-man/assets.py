import pygame
import gameconfig as gc

class Assets:
    def __init__(self):
        self.spritesheet = self.load_spritesheet(gc.SPRITESHEET_PATH, gc.SPRITESHEET_NAME, gc.SPRITESHEET_WIDTH, gc.SPRITESHEET_HEIGHT)

        self.player_character = self.load_sprite_range(gc.PLAYER, self.spritesheet)
        self.hard_block = self.load_sprite_range(gc.HARD_BLOCK, self.spritesheet)
        self.soft_block = self.load_sprite_range(gc.SOFT_BLOCK, self.spritesheet)
        self.background = self.load_sprite_range(gc.BACKGROUND, self.spritesheet)
        self.bomb = self.load_sprite_range(gc.BOMB, self.spritesheet)
        self.explosions = self.load_sprite_range(gc.EXPLOSIONS, self.spritesheet)

        for image_list in ["right_end", "right_mid", "down_end", "down_mid"]:
            self.rotate_images_in_list(self.explosions[image_list], 180)

        self.enemies = {
            "ballom": self.load_sprite_range(gc.BALLOM, self.spritesheet),
            "onil": self.load_sprite_range(gc.ONIL, self.spritesheet),
            "dahl": self.load_sprite_range(gc.DAHL, self.spritesheet),
            "minvo": self.load_sprite_range(gc.MINVO, self.spritesheet),
            "doria": self.load_sprite_range(gc.DORIA, self.spritesheet),
            "ovape": self.load_sprite_range(gc.OVAPE, self.spritesheet),
            "pass": self.load_sprite_range(gc.PASS, self.spritesheet),
            "pontan": self.load_sprite_range(gc.PONTAN, self.spritesheet),
        }

        self.specials = self.load_sprite_range(gc.SPECIALS, self.spritesheet)

    def load_spritesheet(self, path, filename, width, height):
        image = pygame.image.load(f"{path}/{filename}").convert_alpha()
        image = pygame.transform.scale(image, (width, height))

        return image
    
    def load_sprites(self, spritesheet, xCoord, yCoord, width, height):
        image = pygame.Surface((width, height))
        
        image.fill((0,0,1))

        image.blit(spritesheet, (0, 0), (xCoord, yCoord, width, height))

        image.set_colorkey(gc.BLACK)

        return image
    
    def load_sprite_range(self, image_dictionary, spritesheet, row = gc.TILE_SIZE, column = gc.TILE_SIZE, width = gc.TILE_SIZE, height = gc.TILE_SIZE, resize = False):
        animation_images = {}

        for animation in image_dictionary.keys():
            animation_images[animation] = []

            for coord in image_dictionary[animation]:
                image = self.load_sprites(spritesheet, coord[1] * column, coord[0] * row, width, height)

                if resize:
                    image = pygame.transform.scale(image, (32, 32))

                animation_images[animation].append(image)

        return animation_images
    
    def rotate_images_in_list(self, image_list, rotation):
        for ind, image in enumerate(image_list):
            image = pygame.transform.rotate(image, rotation)
            image_list[ind] = image
    
