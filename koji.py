import pygame
import math
import time
pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode([width,height])
clock = pygame.time.Clock()
posx = 0
posy = 0
ifRunning = True
while ifRunning:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ifRunning = False
    screen.fill((255,255,255))
    pygame.draw.circle(screen, (0,0,0), (width/2,height/2), math.sqrt(width+height)/2)
    if keys[pygame.K_w]:
        posy +=1
    if keys[pygame.K_s]:
        posy -=1
    if keys[pygame.K_a]:
        posx -=1
    if keys[pygame.K_d]:
        posx +=1
    pygame.display.flip()

    clock.tick(165)
pygame.quit()
