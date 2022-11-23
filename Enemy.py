import pygame, time

class Enemy:
    def __init__(self, player, vel, x): #May add Attack Speed and Attack Strength
        self.vel = int(vel)
        self.x = int(x)
        self.y = 460
        self.img = pygame.image.load("assets/images/Enemy.png")
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