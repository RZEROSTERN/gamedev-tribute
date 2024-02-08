import pygame
import gameconfig as gc

class GameAssets:
    def __init__(self):
        # Start Screen Assets
        self.start_screen = self.load_ind_img("start_screen", True, (gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT))
        self.start_screen_token = self.load_ind_img("token", True, (gc.IMAGE_SIZE, gc.IMAGE_SIZE))

        self.spritesheet = self.load_ind_img("BattleCity")
        self.number_image_black_white = self.load_ind_img("numbers_black_white")
        self.number_image_black_orange = self.load_ind_img("numbers_black_orange")

        # TODO: Images related to characters

        # TODO: Game related images

        # TODO: Game HUD images

        # TODO: Tile images

        # TODO: Number images

        self.score_sheet_images = {}

        for image in ["hiScore", "arrow", "player1", "player2", "pts", "stage", "total"]:
            self.score_sheet_images[image] = self.load_ind_img(image)

    def load_ind_img(self, path, scale = False, size = (0,0)):
        image = pygame.image.load(f"assets/{path}.png").convert_alpha()

        if scale:
            image = pygame.transform.scale(image, size)
        
        return image