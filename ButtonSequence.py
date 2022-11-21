#Setup
import pygame, sys, time
from pygame.locals import *
pygame.init()
canvas = pygame.display.set_mode((1360, 660))
pygame.display.set_caption("Button Sequence")
main = pygame.image.load("Homescreen.png")
playerimg = pygame.image.load("Player.png")
stoneimg = pygame.image.load("Stone.png")
enemyimg = pygame.image.load("Enemy.png")
finishimg = pygame.image.load("Finish.png")
upimg = pygame.image.load("Up.png")
downimg = pygame.image.load("Down.png")
attackimg = pygame.image.load("Sword.png")
#Classes
class Player:
    def __init__(self, vel=1, health=10):
        self.vel = int(vel)
        self.health=int(health)
        self.y = 460
        self.dieing = False
        self.dietimer = time.time()
    def move(self):
        pass

class Pebble:
    def __init__(self, player, x):
        self.vel = player.vel
        self.x = int(x)
        self.y = 560
        self.img = stoneimg
    def move(self):
        self.x -= self.vel

class Enemy:
    def __init__(self, player, vel, x): #May add Attack Speed and Attack Strength
        self.vel = int(vel)
        self.x = int(x)
        self.y = 460
        self.img = enemyimg
    def move(self):
        self.x -= self.vel

class FinishLine:
    def __init__(self, player, x):
        self.vel = player.vel
        self.x = x
    def move(self):
        self.x -= self.vel

#Variables
down = False #If space key is right now held down
scene = 0 #Scene ID
level = 1
lvlsprites = []
player = Player()
finaldistance = FinishLine(player, 0)
seq = ["j"] #Key: j=jump, d=duck, a=attack, POSSIBLY, g=grab, u=use
seqdict = {"j":upimg, "d":downimg, "a":attackimg}
#MainLoop
while True:
    canvas.fill((255, 255, 255))
    if scene == 0: #Mainscreen
        canvas.blit(main, (0, 0))
    if scene == 1:
        try:
            with open("level" + str(level) + ".lvl", "r") as info:
                txt = info.read()
        except Exception as err:
            print ("ERROR: " + str(err))
        lvlinfo = txt.split("\n")
        for info in lvlinfo:
            if info == "":
                continue
            spritedict = {"Enemy":Enemy, "Pebble":Pebble}
            sprite = info.split(":")
            if sprite[0] == "Player":
                #Player Sprite
                player = Player(*sprite[1:])
            elif sprite[0] == "Sequence":
                #Space Sequence
                seq = sprite[1:]
            elif sprite[0] == "Distance":
                #final distance
                finaldistance = FinishLine(player, int(sprite[1]))
            else:
                #Adds a sprite to sprite list
                lvlsprites.append(spritedict[sprite[0]](player, *sprite[1:]))
        scene = 2
    if scene == 2:
        canvas.blit(playerimg, (200, player.y))
        canvas.blit(finishimg, (finaldistance.x, 0))
        finaldistance.move()
        for i in range(len(seq)):
            canvas.blit(seqdict[seq[i]], (i * 100, 0))
        for sprite in lvlsprites:
            if sprite.x + sprite.img.get_width() > 0 or sprite.x < 1360: #If image is inside of this box
                canvas.blit(sprite.img, (sprite.x, sprite.y))
            sprite.move()
    #Event loop (Only three events, since their is one key)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE and not down:
            down = True
            if scene == 0:
                scene = 1 # This goes to level screen
        elif event.type == KEYUP and event.key == K_SPACE:
            down = False
    pygame.display.update()
