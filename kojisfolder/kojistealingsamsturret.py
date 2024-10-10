# Example file showing a circle moving on screen
import time
from dataclasses import dataclass

import pygame

@dataclass
class GrapeTower:
    pos: pygame.Vector2
    last_fired: float | None = None

    def update_world(self, now, _dt):
        speed = pygame.Vector2(pygame.mouse.get_rel()).length()*5
        if speed>0 and (self.last_fired is None or now > self.last_fired + 0.25):
            mouse_pos = pygame.mouse.get_pos()
            direction = (mouse_pos - self.pos)
            if direction.x != 0 or direction.y != 0:
                direction.normalize_ip()
            projectiles.append(Grape(pos=self.pos.copy(), velocity=direction * speed))
            self.last_fired = now

    def draw(self):
        pygame.draw.circle(screen, 'red', self.pos, 64)


@dataclass
class Grape:
    pos: pygame.Vector2
    velocity: pygame.Vector2

    def update_world(self, _now, dt):
        self.pos += self.velocity * dt

    def draw(self):
        pygame.draw.circle(screen, 'black', self.pos, 8)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_speed = 300
enemies = [GrapeTower(pos=pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2))]
projectiles = []


def update_world(now, dt):
    for enemy in enemies:
        # E.g. create projectiles
        enemy.update_world(now, dt)
    for projectile in projectiles:
        # E.g. update positions, check for collisions
        projectile.update_world(now, dt)


def render():
    pygame.draw.circle(screen, "blue", player_pos, 32)

    for enemy in enemies:
        enemy.draw()

    for projectile in projectiles:
        projectile.draw()

    pygame.display.flip()


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # wipe the last frame
    screen.fill("green")

    # Handle inputs
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] != keys[pygame.K_s] and keys[pygame.K_a] != keys[pygame.K_d]:
        adjust_pythagoras = 0.7071067811865476
    else:
        adjust_pythagoras = 1
    if keys[pygame.K_w]:
        player_pos.y -= player_speed * adjust_pythagoras * dt
    if keys[pygame.K_s]:
        player_pos.y += player_speed * adjust_pythagoras * dt
    if keys[pygame.K_a]:
        player_pos.x -= player_speed * adjust_pythagoras * dt
    if keys[pygame.K_d]:
        player_pos.x += player_speed * adjust_pythagoras * dt

    # Update world
    update_world(time.perf_counter(), dt)

    # Draw the current game state
    render()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()