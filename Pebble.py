import pygame
from Sprite import Sprite

class Pebble(Sprite):
    def __init__(self, speed_multiplier, player, x):
        self.vel = player.vel * speed_multiplier
        self.x = int(x)
        self.y = 560
        self.img = pygame.image.load("assets/images/Stone.png").convert_alpha()
        self.dead = False
        self.damage = 1
        self.needs_hit = True
        self.attackable = False
    def move(self):
        self.x -= self.vel
    def attack(self):
        if self.damage == 1:
            self.damage = 0
            return 1
        return 0
    def impact(self):
        pass
