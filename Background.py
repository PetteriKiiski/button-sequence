import pygame

class Background:
    def __init__(self, img, grnd):
        self.img =  pygame.image.load(img).convert_alpha()
        self.img2 = pygame.image.load(img).convert_alpha()
        self.grnd = pygame.image.load(grnd).convert_alpha()
        self.x1 = 0
        self.x2 = self.img.get_width()

    def move(self, amt):
        self.x1 -= amt
        self.x2 -= amt

        if self.x1 + self.img.get_width() <= 0:
            self.x1 = self.img.get_width()

        if self.x2 + self.img.get_width() <= 0:
            self.x2 = self.img.get_width()