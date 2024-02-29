import pygame
import gameconfig as gc

class Game:
    def __init__(self, main, assets):
        self.main = main
        self.assets = assets

        self.groups = {
            "All_Tanks" : pygame.sprite.Group()
        }

        self.player1 = None
        self.player2 = None

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main.run = False

    def update(self):
        print("Game running")

    def draw(self, window):
        pass