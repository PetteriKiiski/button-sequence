import pygame, time
from Sprite import Sprite
class Enemy(Sprite):
    def __init__(self, speed_multiplier, player, vel, x):
        self.vel = int(vel) * 2 * speed_multiplier
        self.x = int(x)
        self.y = 460
        self.img = pygame.image.load("assets/images/Enemy.png").convert_alpha()
        self.dead = False
        self.damage = 1
        self.attackTimer = time.time()
        self.needs_hit = False
        self.attackable = True
    def move(self):
        self.x -= self.vel
    def attack(self):
        self.vel = 0
        if not self.dead and time.time() - self.attackTimer >= 0.5:
            self.attackTimer = time.time()
            return self.damage
        return 0
    def under_attack(self, damage):
        self.dead = True
