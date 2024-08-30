import pygame
import gameconfig as gc

class Fade:
    def __init__(self, game, assets, speed = 5):
        self.game = game
        self.level = self.game.level_num - 1
        self.assets = assets
        self.images = self.assets.hud_images
        self.speed = speed

        self.fade_active = False
        self.fade_in = True
        self.fade_out = False
        self.transition = False
        self.timer = pygame.time.get_ticks()

        self.top_rect = pygame.Rect(0, 0 - gc.SCREEN_HEIGHT // 2, gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT // 2)
        self.top_rect_start_y = self.top_rect.bottom
        self.top_rect_end_y = gc.SCREEN_HEIGHT // 2
        self.top_y = self.top_rect.bottom

        self.bottom_rect = pygame.Rect(0, gc.SCREEN_HEIGHT, gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT//2)
        self.bottom_rect_start_y = self.bottom_rect.top
        self.bottom_rect_end_y = gc.SCREEN_HEIGHT // 2
        self.bottom_y = self.bottom_rect.top

        self.stage_pic_width, self.stage_pic_height = self.images["stage"].get_size()
        self.num_pic_width, self.num_pic_height = self.images["num_0"].get_size()

        self.stage_image = self.create_stage_image()
        self.stage_image_rect = self.stage_image.get_rect(center = (gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2))

    def update(self):
        if not self.fade_active:
            return
        
        if self.fade_in:
            self.top_y = self.move_y_fade(self.top_y, self.top_rect_start_y, self.top_rect_end_y, self.speed)
            self.top_rect.bottom = self.top_y

            self.bottom_y = self.move_y_fade(self.bottom_y, self.bottom_rect_start_y, self.bottom_rect_end_y, self.speed)
            self.bottom_rect.top = self.bottom_y

            if self.top_rect.bottom == self.top_rect_end_y and self.bottom_rect.top == self.bottom_rect_end_y:
                self.fade_in = False
                self.fade_out = False
                self.transition = True
                self.timer = pygame.time.get_ticks()
                # self.fade_active = False

        elif self.transition:
            if pygame.time.get_ticks() - self.timer >= 1000:
                self.fade_in = False
                self.fade_out = True
                self.transition = False

        elif self.fade_out:
            self.top_y = self.move_y_fade(self.top_y, self.top_rect_end_y, self.top_rect_start_y, self.speed)
            self.top_rect.bottom = self.top_y

            self.bottom_y = self.move_y_fade(self.bottom_y, self.bottom_rect_end_y, self.bottom_rect_start_y, self.speed)
            self.bottom_rect.top = self.bottom_y

            if self.top_rect.bottom == self.top_rect_start_y and self.bottom_rect.top == self.bottom_rect_start_y:
                self.fade_in = True
                self.fade_out = False
                self.transition = False
                self.fade_active = False
                self.game.game_on = True
                return

    def draw(self, window):
        pygame.draw.rect(window, gc.GREY, self.top_rect)
        pygame.draw.rect(window, gc.GREY, self.bottom_rect)

        if self.transition:
            window.blit(self.stage_image, self.stage_image_rect)

    def move_y_fade(self, y_coord, start_pos, end_pos, speed):
        if start_pos > end_pos:
            y_coord -= speed

            if y_coord - end_pos < 0:
                y_coord = end_pos
        elif start_pos < end_pos:
            y_coord += speed
            
            if y_coord > end_pos:
                y_coord = end_pos

        return y_coord
    
    def create_stage_image(self):
        surface = pygame.Surface((self.stage_pic_width + (self.num_pic_width * 3), self.stage_pic_height))
        surface.fill(gc.GREY)
        surface.blit(self.images["stage"], (0,0))

        if self.level < 10:
            surface.blit(self.images["num_0"], (self.stage_pic_width + self.num_pic_width, 0))
        else:
            surface.blit(self.images[f"num_{str(self.level)[0]}"], (self.stage_pic_width + self.num_pic_width, 0))

        surface.blit(self.images[f"num_{str(self.level)[-1]}"], (self.stage_pic_width + (self.num_pic_width * 2), 0))

        return surface

        
