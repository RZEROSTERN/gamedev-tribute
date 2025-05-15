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
        self.animation_time = 50
        self.animation_time_set = pygame.time.get_ticks()
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
            self.move("walk_right")
        elif keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.move("walk_left")
        elif keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            self.move("walk_up")
        elif keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
            self.move("walk_down")

        self.rect.topleft = (self.x, self.y)

    def update(self):
        pass

    def draw(self, window):
        window.blit(self.image, self.rect)
        pygame.draw.rect(window, gc.RED, self.rect, 1)

    def animate(self, action):
        if pygame.time.get_ticks() - self.animation_time_set >= self.animation_time:
            self.index += 1

            if self.index == len(self.image_dictionary[action]):
                self.index = 0
                # self.index = self.index % len(self.image_dictionary[action])

            self.image = self.image_dictionary[action][self.index]
            self.animation_time_set = pygame.time.get_ticks()

    def move(self, action):
        if not self.alive:
            return
        
        if action != self.action:
            self.action = action
            self.index = 0
        
        direction = {"walk_left": -self.speed, "walk_right": self.speed, "walk_up": -self.speed, "walk_down": self.speed}

        if action == "walk_left" or action == "walk_right":
            self.x += direction[action]
        elif action == "walk_up" or action == "walk_down":
            self.y += direction[action]

        self.animate(action)

        self.rect.topleft = (self.x, self.y)