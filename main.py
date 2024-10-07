import pygame
import math
import time
pygame.init()
screen = pygame.display.set_mode([500,500])
clock = pygame.time.Clock()
ifRunning = True
while ifRunning:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ifRunning = False
    screen.fill((255,255,255))
    pygame.draw.circle(screen, (0,0,0), (250,250), 25)
    if keys[pygame.K_e]:
        ifRunning = False
    pygame.display.flip()
    clock.tick(165)
pygame.quit()
