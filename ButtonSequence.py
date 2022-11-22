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
YouLose = pygame.image.load("YouLose.png")
YouWin = pygame.image.load("YouWin.png")
notes = pygame.image.load("Notes.png")
#Classes
class Player:
    def __init__(self, vel=1, health=10):
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
    def move(self):
        if self.jumping:
            self.y = 260
            if time.time() - self.jumptimer >= self.timing:
                self.jumping = False
        elif self.ducking:
            self.y = 560
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
        for sprite in lvlsprites:
            if sprite.attackable and((600 > sprite.x and 600 < sprite.x + sprite.img.get_width()) or (500 > sprite.x and 500 < sprite.img.get_width())): #Ensuring enemy should get attacked
                sprite.under_attack(1)

class Pebble:
    def __init__(self, player, x):
        self.vel = player.vel
        self.x = int(x)
        self.y = 560
        self.img = stoneimg
        self.dead = False
        self.damage = 1
        self.needs_hit = True
        self.attackable = False
    def move(self):
        self.x -= self.vel
    def attack(self):
        if self.damage == 1:
            self.damage = 0
            return 1
        return 0

class Enemy:
    def __init__(self, player, vel, x): #May add Attack Speed and Attack Strength
        self.vel = int(vel)
        self.x = int(x)
        self.y = 460
        self.img = enemyimg
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
world = 1
maxlevelworld = [1, 1]
absolutelevelworld = [1, 1]
lvlsprites = []
player = Player()
finaldistance = FinishLine(player, 0)
seq = ["j"] #Key: j=jump, d=duck, a=attack, POSSIBLY, g=grab, u=use
seqindex = 0
seqdict = {"j":upimg, "d":downimg, "a":attackimg}
font = pygame.font.Font("freesansbold.ttf", 100)
clock = pygame.time.Clock()
leveltimer = time.time()
#MainLoop
while True:
    timer = time.time()
    canvas.fill((255, 255, 255))
    if scene == 0: #Mainscreen
        canvas.blit(main, (0, 0))
    if scene == 0.5:
        canvas.blit(notes, (0, 0))
    if scene == 1:
        levelimg = pygame.image.load("LevelTemplate" + str(level) + ".png")
        canvas.blit(levelimg, (0, 0))
        text = font.render("World " + str(world), True, (0, 0, 0), None)
        canvas.blit(text, (0, 0))
        text = font.render("Press space to next level", True, (0, 0, 0), None)
        canvas.blit(text, (0, 250))
        text = font.render("or wait to start", True, (0, 0, 0), None)
        canvas.blit(text, (0,350))
        if time.time() - leveltimer >= 3:
            level = 1
            lvlsprites = []
            player = Player()
            finaldistance = FinishLine(player, 0)
            seq = ["j"] #Key: j=jump, d=duck, a=attack, POSSIBLY, g=grab, u=use
            seqindex = 0
            seqdict = {"j":upimg, "d":downimg, "a":attackimg}
            font = pygame.font.Font("freesansbold.ttf", 100)
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
        player.move()
        canvas.blit(finishimg, (finaldistance.x, 0))
        finaldistance.move()
        for i in range(len(seq)):
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
                if level > maxlevelworld[0]:
                    level = 1
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
