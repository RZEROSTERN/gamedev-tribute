import pygame
import gameconfig as gc
from gameassets import GameAssets

class Main:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT))
        pygame.display.set_caption(gc.GAME_TITLE)

        self.Clock = pygame.time.Clock()
        self.run = True

        self.assets = GameAssets()

    def run_game(self):
        while self.run:
            self.input()
            self.update()
            self.render()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def update(self):
        pass

    def render(self):
        self.screen.fill(gc.BLACK)

        pygame.display.update()

if __name__ == "__main__":
    chess = Main()
    chess.run_game()
    pygame.quit()