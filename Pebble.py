import pygame

class Pebble:
    def __init__(self, player, x):
        self.vel = player.vel
        self.x = int(x)
        self.y = 560
        self.img = pygame.image.load("assets/images/Stone.png")
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