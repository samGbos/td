"""
Seiji Ting 10/7/24
Used sam's code as framework in order to try and implement acceleration
(smooth movement) This might be useful for projectiles, depending on what
we decide to do with the game.

Moving forward:
bouncing ball
collision detection
etc.
"""
# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
acceleration = -100; #units per tick
xvel = 0.0
yvel= 0.0
xdist = 0.0
ydist = 0.0
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.circle(screen, "red", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        yvel = -300
    if keys[pygame.K_s]:
        yvel = 300
    if keys[pygame.K_a]:
        xvel = -300
    if keys[pygame.K_d]:
        xvel = 300

    #d = Vt + 1/2 (a)(t)^2
    #t = dt
    # update player distances
    ydist = yvel*dt
    xdist = xvel*dt

    #update player positions (x+ right, y+ down)
    player_pos.y += ydist #(down)
    player_pos.x += xdist #(right)

    #update player velocities
    #Vf = Vi + at

    yvel = round(yvel*0.9,1)
    xvel = round(xvel*0.9,1)

    #reset velocities, no acceleration (consider making upper limit values with ABS)
    #xvel = 0
    #yvel = 0

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()