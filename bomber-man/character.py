import pygame
import gameconfig as gc

class Character(pygame.sprite.Sprite):
    def __init__(self, game, image_dictionary):
        super().__init__()
        self.game = game

        self.x = 0
        self.y = 0

        self.alive = True
        self.speed = 3
        
        self.action = "walk_left"

        self.index = 0
        self.image_dictionary = image_dictionary
        self.image = self.image_dictionary[self.action][self.index] #Definitive image. Still not implemented.
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.main.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.main.run = False

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.x += self.speed
        elif keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.x -= self.speed
        elif keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            self.y -= self.speed
        elif keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
            self.y += self.speed

        self.rect.topleft = (self.x, self.y)

    def update(self):
        pass

    def draw(self, window):
        window.blit(self.image, self.rect)
        pygame.draw.rect(window, gc.RED, self.rect, 1)