import pygame
import math
import time
pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode([width,height])
clock = pygame.time.Clock()
posx = width/2
posy = height/2
gravity = 0.5
vely = 0
jumpStrength = -15
onGround = False
radius = 25
rectWidth = width
rectHeight = 35
rectx = 0
recty = height - rectHeight
speedx = 5
def jumping():
    global vely, onGround #global variable necessary so jump can be accessible throughout program
    vely = jumpStrength
    onGround = False
pygame.draw.circle(screen, (0,0,0), (width/2,height/2), math.sqrt(width+height)/2)
ifRunning = True
while ifRunning:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ifRunning = False
    if onGround and keys[pygame.K_w]:
        jumping()
    if onGround and keys[pygame.K_SPACE]:
        jumping()
    if posx>0 and keys[pygame.K_a]:
        posx -= speedx
    if posx<width and keys[pygame.K_d]:
        posx += speedx
    vely += gravity #adds gravity to velocity y
    posy += vely #changes position by amount velocity y
    if posy + radius >= recty:
        posy = recty - radius
        vely = 0
        onGround = True
    else:
        onGround = False
    screen.fill((255,255,255))
    pygame.draw.circle(screen, (0,0,0), (posx,posy), radius)
    pygame.draw.rect(screen, (0,0,0), (rectx,recty,rectWidth,rectHeight))
    pygame.display.flip()
    clock.tick(165)
pygame.quit()