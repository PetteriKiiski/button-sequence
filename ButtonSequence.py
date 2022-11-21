#Setup
import pygame, sys
from pygame.locals import *
pygame.init()
canvas = pygame.display.set_mode((1360, 660))
pygame.display.set_caption("Button Sequence")
main = pygame.image.load("Homescreen.png")
playerimg = pygame.image.load("Player.png")
stoneimg = pygame.image.load("Stone.png")
enemyimg = pygame.image.load("Enemy.png")
#Classes
class Player:
    def __init__(self, vel=1, health=10):
        self.vel = int(vel)
        self.health=int(health)
        self.y = 460

class Pebble:
    def __init__(self, player, x):
        self.vel = player.vel
        self.x = int(x)
        self.y = 560
        self.img = stoneimg

class Enemy:
    def __init__(self, player, vel, x): #May add Attack Speed and Attack Strength
        self.vel = int(vel)
        self.x = int(x)
        self.y = 460
        self.img = enemyimg
#Variables
down = False #If space key is right now held down
scene = 0 #Scene ID
level = 1
distance = 0
finaldistance = 0
lvlsprites = []
player = Player()
seq = ["j"] #Key: j=jump, d=duck, a=attack, POSSIBLY, g=grab, u=use
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
                finaldistance = int(sprite[1])
            else:
                #Adds a sprite to sprite list
                lvlsprites.append(spritedict[sprite[0]](player, *sprite[1:]))
        scene = 2
    if scene == 2:
        canvas.blit(playerimg, (200, player.y))
        for sprite in lvlsprites:
#            if sprite.x + sprite.img.get_width() < 0 or sprite.x - sprite.img.get_width() > 1360: #If image is inside of this box
            canvas.blit(sprite.img, (sprite.x, sprite.y))
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
