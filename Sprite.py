#General class for enemy sprites: ex. Pebbles, Enemies
import pygame

class Sprite:
    def __init__(self, player, *info, x):
        self.x = x
        self.vel = player.vel

    def move(self):
        self.x -= self.vel

    def attack(self):
        pass
    
    def under_attack(self):
        pass

    def impact(self):
        pass