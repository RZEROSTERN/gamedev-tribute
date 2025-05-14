import pygame
import gameconfig as gc

class Main:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT))
        self.fps = pygame.time.Clock()

        pygame.display.set_caption(gc.GAME_TITLE)

        self.run = True

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def update(self):
        self.fps.tick(gc.FPS)

    def draw(self, window):
        window.fill(gc.BLACK)
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