#Setup

import pygame, sys, time
from pygame.locals import *

from Player import Player
from Pebble import Pebble
from Enemy import Enemy
from FinishLine import FinishLine

pygame.init()
canvas = pygame.display.set_mode((1360, 660))
pygame.display.set_caption("assets/images/Button Sequence")
main = pygame.image.load("assets/images/Homescreen.png")
playerimg = pygame.image.load("assets/images/Player.png")
finishimg = pygame.image.load("assets/images/Finish.png")
upimg = pygame.image.load("assets/images/Up.png")
downimg = pygame.image.load("assets/images/Down.png")
attackimg = pygame.image.load("assets/images/Sword.png")
highupimg = pygame.image.load("assets/images/HighUp.png")
highdownimg = pygame.image.load("assets/images/HighDown.png")
highattackimg = pygame.image.load("assets/images/HighSword.png")
YouLose = pygame.image.load("assets/images/YouLose.png")
YouWin = pygame.image.load("assets/images/YouWin.png")
notes = pygame.image.load("assets/images/Notes.png")

#Variables
down = False #If space key is right now held down
scene = 0 #Scene ID
level = 1
world = 1
maxlevelworld = [10, 1]
absolutelevelworld = [10, 1]
lvlsprites = []
player = Player(lvlsprites)
finaldistance = FinishLine(player, 0)
seq = ["j"] #Key: j=jump, d=duck, a=attack, POSSIBLY, g=grab, u=use
seqindex = 0
seqdict = {"j":upimg, "d":downimg, "a":attackimg}
highseqdict = {"j": highupimg, "d":highdownimg, "a":highattackimg}
font = pygame.font.Font("freesansbold.ttf", 100)
clock = pygame.time.Clock()
leveltimer = time.time()

def paintMap(level):
    startX = 0
    startY = 0

    intX = 180
    intY = 160

    for x in range(0, 10):
        levelimg = pygame.image.load("assets/images/Level.png")
       
        if level == x+1:
             levelimg = pygame.image.load("assets/images/LevelPick.png")

        canvas.blit(levelimg, ((startX + intX * (x%5)),
                                     startY + ((int(x/5)) * intY)))

#MainLoop
while True:
    timer = time.time()
    canvas.fill((255, 255, 255))
    if scene == 0: #Mainscreen
        canvas.blit(main, (0, 0))
    if scene == 0.5:
        canvas.blit(notes, (0, 0))
    if scene == 1:
        paintMap(level)
        text = font.render("World " + str(world), True, (0, 0, 0), None)
        canvas.blit(text, (0, 0))
        text = font.render("Press space to next level", True, (0, 0, 0), None)
        canvas.blit(text, (0, 250))
        text = font.render("or wait to start", True, (0, 0, 0), None)
        canvas.blit(text, (0,350))
        if time.time() - leveltimer >= 1.5:
            level += (world - 1) * 10
            lvlsprites = []
            player = Player(lvlsprites)
            finaldistance = FinishLine(player, 0)
            seq = ["j"] #Key: j=jump, d=duck, a=attack, POSSIBLY, g=grab, u=use
            seqindex = 0
            seqdict = {"j":upimg, "d":downimg, "a":attackimg}
            font = pygame.font.Font("freesansbold.ttf", 100)
            try:
                with open("assets/level" + str(level) + ".lvl", "r") as info:
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
                   player = Player(lvlsprites, *sprite[1:])
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
        player.move()
        canvas.blit(finishimg, (finaldistance.x, 0))
        finaldistance.move()
        for i in range(len(seq)):
            if i == seqindex:
                canvas.blit(highseqdict[seq[i]], (i * 100, 0))
            else:
                canvas.blit(seqdict[seq[i]], (i * 100, 0))
        text = font.render("Health: " + str(player.health), True, (0, 0, 0), None)
        canvas.blit(text, (0, 100))
        for sprite in lvlsprites:
            if (sprite.x + sprite.img.get_width() > 0 or sprite.x < 1360) and not sprite.dead: #If image is inside of this box
                canvas.blit(sprite.img, (sprite.x, sprite.y))
            sprite.move()
            playerRect = pygame.Rect(200, player.y, 200, 200)
            spriteRect = pygame.Rect(sprite.x, sprite.y, sprite.img.get_width(), sprite.img.get_height())
            if sprite.needs_hit and playerRect.colliderect(spriteRect):
                player.health -= sprite.attack()
            elif not sprite.needs_hit and 400 > sprite.x and 400 < sprite.x + sprite.img.get_width(): #If the x is in enemy's range
                player.health -= sprite.attack()
        if player.health <= 0:
            scene = 3
        if 200 >= finaldistance.x:
            scene = 4
            if maxlevelworld != absolutelevelworld and level == maxlevelworld[0] and world == maxlevelworld[1]:
                if maxlevelworld[0] == 10:
                    maxlevelworld[0] = 1
                    maxlevelworld[1] += 1
                else:
                    maxlevelworld[0] += 1
    if scene == 3:
        canvas.blit(YouLose, (0, 0))
    if scene == 4:
        canvas.blit(YouWin, (0, 0))
    #Event loop (Only three events, since their is one key)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE and not down:
            down = True
            if scene == 0:
                scene = 0.5
            elif scene == 0.5:
                scene = 1
                leveltimer = time.time()
            elif scene == 1:
                level += 1
                if level > maxlevelworld[0] and world == maxlevelworld[1]:
                    level = 1
                    world = 1
                leveltimer = time.time()
            elif scene == 2:
                if seq[seqindex] == "j":
                    player.jump()
                if seq[seqindex] == "d":
                    player.duck()
                if seq[seqindex] == "a":
                    player.attack()
                seqindex += 1
                if seqindex >= len(seq):
                    seqindex = 0
            elif scene == 3:
                scene = 1
                leveltimer = time.time()
            elif scene == 4:
                scene = 1
                leveltimer = time.time()
        elif event.type == KEYUP and event.key == K_SPACE:
            down = False
    clock.tick(60)
    pygame.display.update()