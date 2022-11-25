import pygame

class FinishLine:
    def __init__(self, player, speed_multiplier, x):
        self.img = pygame.image.load("assets/images/Finish.png").convert_alpha()
        self.vel = player.vel * speed_multiplier
        self.x = x
    def move(self):
        self.x -= self.vel