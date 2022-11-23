import pygame, time

class Player:
    def __init__(self, lvlsprites, vel=1, health=10):
        self.lvlsprites = lvlsprites
        self.vel = int(vel)
        self.health=int(health)
        self.y = 460
        self.timing = 3
        self.dieing = False
        self.jumping = False
        self.ducking = False
        self.contact = False
        self.dietimer = time.time()
        self.jumptimer = time.time()
        self.img = pygame.image.load("assets/images/Player.png")

    def move(self):
        self.img = pygame.image.load("assets/images/Player.png")
        if self.jumping:
            self.y = 260
            if time.time() - self.jumptimer >= self.timing:
                self.jumping = False
        elif self.ducking:
            self.y = 560
            self.img = pygame.image.load("assets/images/PlayerSquish.png")
            if time.time() - self.ducktimer >= self.timing:
                self.ducking = False
        else:
            self.y = 460

    def jump(self):
        self.jumping = True
        self.ducking = False
        self.jumptimer = time.time()

    def duck(self):
        self.ducking = True
        self.jumping = False
        self.ducktimer = time.time()

    def attack(self):
        attacked = False
        for sprite in self.lvlsprites:
            if sprite.attackable and 600 > sprite.x and not sprite.dead: #Ensuring enemy should get attacked
                sprite.under_attack(1)
                break