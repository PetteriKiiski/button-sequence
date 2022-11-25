import pygame
from Sprite import Sprite

class Bird(Sprite):
    def __init__(self, speed_multiplier, player, vel, x):
        self.vel = int(vel) * (speed_multiplier ** 2)
        self.playervel = player.vel * speed_multiplier
        self.yvel = 0
        self.x = int(x)
        self.y = 410
        self.img = pygame.image.load("assets/images/Bird.png")
        self.dead = False
        self.damage = 1
        self.needs_hit = True
        self.attackable = False
    def move(self):
        self.x -= self.vel
        self.y += self.yvel
    def attack(self):
        if self.damage == 1:
            self.damage = 0
            return 1
        return 0
    def impact(self):
        self.yvel = self.playervel