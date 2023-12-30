import pygame, sys, random
from game import Game

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50

GREY = (29, 29, 27)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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

    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.lasers_group.draw(screen)

    for shield in game.shields:
        shield.blocks_group.draw(screen)

    game.aliens_group.draw(screen)
    game.alien_lasers_group.draw(screen)
    game.mistery_ship_group.draw(screen)


    pygame.display.update()
    clock.tick(60)