import pygame
import gameconfig as gc
from assets import Assets
from game import Game

class Main:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT))

        self.assets = Assets()  # Placeholder for assets
        self.game = Game(self, self.assets)
        self.fps = pygame.time.Clock()

        pygame.display.set_caption(gc.GAME_TITLE)

        self.run = True

    def input(self):
        self.game.input()

    def update(self):
        self.fps.tick(gc.FPS)

    def draw(self, window):
        window.fill(gc.BLACK)
        self.game.draw(window)
        pygame.display.update()

    def run_game(self):
        while self.run:
            self.input()
            self.update()
            self.draw(self.screen)

if __name__ == "__main__":
    bomberman = Main()
    bomberman.run_game()
    pygame.quit()