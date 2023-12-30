import pygame, sys, random
from game import Game

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50

GREY = (29, 29, 27)
YELLOW = (243, 216, 63)

font = pygame.font.Font("assets/fonts/monogram.ttf", 40)
level_surface = font.render("LEVEL 01", False, YELLOW)
game_over_surface = font.render("GAME OVER", False, YELLOW)
score_text_surface = font.render("SCORE", False, YELLOW)
high_score_text_surface = font.render("HIGH SCORE", False, YELLOW)

screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2 * OFFSET))
pygame.display.set_caption("Space Invaders")

clock = pygame.time.Clock()

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)

SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, 300)

MISTERYSHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MISTERYSHIP, random.randint(4000, 8000))

# Game loop
while True:
    # Event check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SHOOT_LASER and game.run:
            game.alien_shoot_laser()

        if event.type == MISTERYSHIP and game.run:
            game.create_mistery_ship()
            pygame.time.set_timer(MISTERYSHIP, random.randint(4000, 8000))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and game.run == False:
            game.reset()

    if game.run:
        game.spaceship_group.update()
        game.alien_lasers_group.update()
        game.mistery_ship_group.update()
        game.check_for_collisions()
        game.move_aliens()

    screen.fill(GREY)
    pygame.draw.rect(screen, YELLOW, (10,10, 780, 780), 2, 0, 60, 60, 60, 60)
    pygame.draw.line(screen, YELLOW, (25, 730), (775,730), 3)

    if game.run:
        screen.blit(level_surface, (570, 740, 50, 50))
    else:
        screen.blit(game_over_surface, (570, 740, 50, 50))

    lives_offset = 50
    for life in range(game.lives):
        screen.blit(game.spaceship_group.sprite.image, (lives_offset, 745))
        lives_offset += 50

    screen.blit(score_text_surface, (50, 15, 50, 50))

    formatted_score = str(game.score).zfill(5)
    score_surface = font.render(formatted_score, False, YELLOW)

    formatted_high_score = str(game.highscore).zfill(5)
    high_score_surface = font.render(formatted_high_score, False, YELLOW)

    screen.blit(score_surface, (50, 40, 50, 50))
    screen.blit(high_score_text_surface, (550, 15, 50, 50))
    screen.blit(high_score_surface, (625, 40, 50, 50))

    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.lasers_group.draw(screen)

    for shield in game.shields:
        shield.blocks_group.draw(screen)

    game.aliens_group.draw(screen)
    game.alien_lasers_group.draw(screen)
    game.mistery_ship_group.draw(screen)


    pygame.display.update()
    clock.tick(60)