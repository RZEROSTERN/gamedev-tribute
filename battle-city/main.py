import pygame
import gameconfig as gc
from gameassets import GameAssets

class Main:
    
    def __init__(self):
        # Main Game Obj
        pygame.init()

        self.screen = pygame.display.set_mode((gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT))
        pygame.display.set_caption("Battle City")

        self.Clock = pygame.time.Clock()
        self.run = True
        
        self.assets = GameAssets()

    def run_game(self):
        # The Game Loop
        while self.run:
            self.input()
            self.update()
            self.render()

    def input(self):
        # Input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def update(self):
        # Update the game
        self.Clock.tick(gc.FPS)

    def render(self):
        # Handle all of the assets
        self.screen.fill(gc.BLACK)
        self.screen.blit(self.assets.tank_images["Tank_4"]["Green"]["Down"][0], (400,400))
        pygame.display.update()

if __name__ == "__main__":
    battleCity = Main()
    battleCity.run_game()
    pygame.quit()
        
