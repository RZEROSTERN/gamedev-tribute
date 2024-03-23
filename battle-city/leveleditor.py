import pygame
import gameconfig as gc


class LevelEditor:
    def __init__(self, main, assets):
        self.main = main
        self.assets = assets
        self.active = True

        self.level_data = None
        self.all_levels = []
        self.overlay_screen = self.draw_screen()
        self.matrix = self.create_level_matrix()

        self.brick_image = self.assets.brick_tiles["small"]
        self.steel_image = self.assets.steel_tiles["small"]

        self.tile_type = {
            432: self.assets.brick_tiles["small"],
            482: self.assets.steel_tiles["small"],
            483: self.assets.forest_tiles["small"],
            484: self.assets.ice_tiles["small"],
            533: self.assets.water_tiles["small_1"],
            999: self.assets.flag["Phoenix_Alive"]
        }

        self.icon_image = self.assets.tank_images["Tank_4"]["Gold"]["Up"][0]
        self.icon_rect = self.icon_image.get_rect(topleft=(gc.SCREEN_BORDER_LEFT, gc.SCREEN_BORDER_TOP))

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main.run = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.icon_rect.x += gc.IMAGE_SIZE
                    if self.icon_rect.x >= gc.SCREEN_BORDER_RIGHT:
                        self.icon_rect.x = gc.SCREEN_BORDER_RIGHT - gc.IMAGE_SIZE
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.icon_rect.x -= gc.IMAGE_SIZE
                    if self.icon_rect.x <= gc.SCREEN_BORDER_LEFT:
                        self.icon_rect.x = gc.SCREEN_BORDER_LEFT

                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.icon_rect.y += gc.IMAGE_SIZE
                    if self.icon_rect.y >= gc.SCREEN_BORDER_BOTTOM:
                        self.icon_rect.y = gc.SCREEN_BORDER_BOTTOM - gc.IMAGE_SIZE
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.icon_rect.y -= gc.IMAGE_SIZE
                    if self.icon_rect.y <= gc.SCREEN_BORDER_TOP:
                        self.icon_rect.y = gc.SCREEN_BORDER_TOP

    def update(self):
        pass

    def draw(self, window):
        window.blit(self.overlay_screen, (0, 0))
        self.draw_grid_to_screen(window)
        window.blit(self.icon_image, self.icon_rect)
        pygame.draw.rect(window, gc.GREEN, self.icon_rect, 1)

    def draw_screen(self):
        overlay_screen = pygame.Surface((gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT))
        overlay_screen.fill((gc.GREY))
        pygame.draw.rect(overlay_screen, gc.BLACK, (gc.GAME_SCREEN))
        return overlay_screen

    def draw_grid_to_screen(self, window):
        vert_lines = (gc.SCREEN_BORDER_RIGHT - gc.SCREEN_BORDER_LEFT) // gc.IMAGE_SIZE
        hor_lines = (gc.SCREEN_BORDER_BOTTOM - gc.SCREEN_BORDER_TOP) // gc.IMAGE_SIZE

        for i in range(vert_lines):
            pygame.draw.line(window, gc.RED,
                             (gc.SCREEN_BORDER_LEFT + (i * gc.IMAGE_SIZE), gc.SCREEN_BORDER_TOP),
                             (gc.SCREEN_BORDER_LEFT + (i * gc.IMAGE_SIZE), gc.SCREEN_BORDER_BOTTOM))

        for i in range(hor_lines):
            pygame.draw.line(window, gc.RED, (gc.SCREEN_BORDER_LEFT, gc.SCREEN_BORDER_TOP + (i * gc.IMAGE_SIZE)),
                             (gc.SCREEN_BORDER_RIGHT, gc.SCREEN_BORDER_TOP + (i * gc.IMAGE_SIZE)))

    def create_level_matrix(self):
        rows = (gc.SCREEN_BORDER_BOTTOM - gc.SCREEN_BORDER_TOP) // (gc.IMAGE_SIZE // 2)
        cols = (gc.SCREEN_BORDER_RIGHT - gc.SCREEN_BORDER_LEFT) // (gc.IMAGE_SIZE // 2)
        matrix = []

        for row in range(rows):
            line = []
            for col in range(cols):
                line.append(-1)
            matrix.append(line)

        return matrix
