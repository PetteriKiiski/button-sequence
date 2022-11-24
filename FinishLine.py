import pygame

class FinishLine:
    def __init__(self, player, x):
        self.img = pygame.image.load("assets/images/Finish.png").convert_alpha()
        self.vel = player.vel
        self.x = x
    def move(self):
        self.x -= self.vel