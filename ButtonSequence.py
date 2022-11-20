import pygame, sys
from pygame.locals import *
pygame.init()
canvas = pygame.display.set_mode((1360, 660))
pygame.display.set_caption("Button Sequence")
main = pygame.image.load("Homescreen.png")
down = False
scene = 0
while True:
    if scene == 0:
        canvas.blit(main, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE and not down:
            print ("space")
            down = True
        elif event.type == KEYUP and event.key == K_SPACE:
            print ("up")
            down = False
    pygame.display.update()
