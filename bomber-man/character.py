import pygame
import gameconfig as gc

class Character(pygame.sprite.Sprite):
    def __init__(self, game, image_dictionary, group, row_number, column_number, size):
        super().__init__(group)
        self.game = game

        self.row_number = row_number
        self.column_number = column_number
        self.size = size

        self.x = self.column_number * self.size
        self.y = (self.row_number * self.size) + gc.Y_OFFSET

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
        
        self.snap_to_grid()
        self.play_area_restriction(64, (gc.COLUMNS - 1) * 64, gc.Y_OFFSET + 64, ((gc.ROWS - 1) * 64) + gc.Y_OFFSET)

        self.rect.topleft = (self.x, self.y)

        self.collision_detection_items(self.game.groups["hard_blocks"])
        self.collision_detection_items(self.game.groups["soft_blocks"])

        

    def collision_detection_items(self, item_list):
        for item in item_list:
            if self.rect.colliderect(item.rect) and item.passable == False:
                if self.action == "walk_left":
                    if self.rect.left < item.rect.right:
                        self.rect.left = item.rect.right
                        self.x, self.y = self.rect.topleft
                        return
                if self.action == "walk_right":
                    if self.rect.right > item.rect.left:
                        self.rect.right = item.rect.left
                        self.x, self.y = self.rect.topleft
                        return
                
                if self.action == "walk_up":
                    if self.rect.top < item.rect.bottom:
                        self.rect.top = item.rect.bottom
                        self.x, self.y = self.rect.topleft
                        return
                if self.action == "walk_down":
                    if self.rect.bottom > item.rect.top:
                        self.rect.bottom = item.rect.top
                        self.x, self.y = self.rect.topleft
                        return
                    
    def snap_to_grid(self):
        x_pos = self.x % gc.TILE_SIZE
        y_pos = (self.y - gc.Y_OFFSET) % gc.TILE_SIZE

        if self.action in ["walk_up", "walk_down"]:
            if x_pos <= 12:
                self.x = self.x - x_pos
            if x_pos >= 52:
                self.x = self.x + (gc.TILE_SIZE - x_pos)
        elif self.action in ["walk_left", "walk_right"]:
            if y_pos <= 12:
                self.y = self.y - y_pos
            if y_pos >= 52:
                self.y = self.y + (gc.TILE_SIZE - y_pos)

    def play_area_restriction(self, left_x, right_x, top_y, bottom_y):
        if self.x < left_x:
            self.x = left_x
        elif self.x > right_x:
            self.x = right_x

        if self.y < top_y:
            self.y = top_y
        elif self.y > bottom_y:
            self.y = bottom_y
