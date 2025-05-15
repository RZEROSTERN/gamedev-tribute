import pygame
import gameconfig as gc
from character import Character

class Game:
    def __init__(self, main, assets):
        self.main = main
        self.assets = assets

        self.player = Character(self, self.assets.player_character)

    def input(self):
        self.player.input()

    def update(self):
        self.player.update()

    def draw(self, window):
        self.player.draw(window)