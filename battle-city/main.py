import pygame
import gameconfig as gc
from gameassets import GameAssets
from game import Game

class Main:
    def __init__(self):
        # Main Game Obj
        pygame.init()

        self.screen = pygame.display.set_mode((gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT))
        pygame.display.set_caption("Battle City")

        self.Clock = pygame.time.Clock()
        self.run = True
        
        self.assets = GameAssets()

        self.game_on = True
        self.game = Game(self, self.assets, True, False)

    def run_game(self):
        # The Game Loop
        while self.run:
            self.input()
            self.update()
            self.render()

    def input(self):
        if self.game_on:
            self.game.input()
        
        # Input handling
        if not self.game_on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

    def update(self):
        # Update the game
        self.Clock.tick(gc.FPS)

        if self.game_on:
            self.game.update()

    def render(self):
        # Handle all of the assets
        self.screen.fill(gc.BLACK)
        
        if self.game_on:
            self.game.draw(self.screen)

        pygame.display.update()

if __name__ == "__main__":
    battleCity = Main()
    battleCity.run_game()
    pygame.quit()
        
