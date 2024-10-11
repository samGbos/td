# Example file showing a circle moving on screen
import time
from dataclasses import dataclass

import pygame
from pygame import Vector2

GAME_WIDTH = 1280
GAME_HEIGHT = 720


def is_offscreen(pos):
    """
    Return True if this obj is off-screen and should be deleted.
    Intended for use with various kinds of projectiles
    """
    margin = 100
    return (
        pos.x < -margin
        or pos.x > GAME_WIDTH + margin
        or pos.y < -margin
        or pos.y > GAME_HEIGHT + margin
    )


class GrapeTower(pygame.sprite.Sprite):
    last_fired: float | None = None

    def __init__(self, pos: Vector2):
        super().__init__()
        self.image = pygame.Surface([64, 64])
        self.image.fill('red')
        self.rect = pygame.rect.Rect(pos.x, pos.y, self.image.get_width(), self.image.get_height())

    def update(self, game, now, _dt):
        if self.last_fired is None or now > self.last_fired + 1:
            dir_x = game.player.rect.center[0] - self.rect.center[0]
            dir_y = game.player.rect.center[1] - self.rect.center[1]
            direction = pygame.Vector2(dir_x, dir_y)
            if direction.length_squared():
                direction.normalize_ip()
            game.projectiles.add(Grape(pos=Vector2(self.rect.center), velocity=direction * 500))
            self.last_fired = now

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Grape(pygame.sprite.Sprite):
    def __init__(self, pos: Vector2, velocity: Vector2):
        super().__init__()
        self.image = pygame.Surface([8, 8])
        self.image.fill('black')

        self.rect = pygame.rect.Rect(pos.x, pos.y, self.image.get_width(), self.image.get_height())

        self.velocity = velocity
        self.pending_removal = False

    def update(self, game, _now, dt):
        if self.pending_removal or is_offscreen(self.rect) or self.velocity.length_squared() == 0:
            self.kill()
            return

        dpos = self.velocity * dt
        self.rect.x += dpos.x
        self.rect.y += dpos.y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([64, 64])
        self.image.fill('blue')
        self.rect = pygame.rect.Rect(x, y, self.image.get_width(), self.image.get_height())

        self.hp = 100
        self.speed = 300

    def add_hp(self, amount):
        self.hp += amount
        if self.hp <= 0:
            self.image.fill('red')
        else:
            self.image.fill('blue')

    def draw(self, screen):
        screen.blit(self.image, self.rect)


@dataclass
class Game:
    player: Player
    enemies: pygame.sprite.Group
    projectiles: pygame.sprite.Group


def update(game: Game, now, dt):
    for enemy in game.enemies:
        enemy.update(game, now, dt)

    for projectile in game.projectiles:
        projectile.update(game, now, dt)

    collided_projectiles = pygame.sprite.spritecollide(game.player, game.projectiles, False)
    for collided_projectile in collided_projectiles:
        collided_projectile.pending_removal = True
        game.player.add_hp(-10)


def draw(game, screen):
    for enemy in game.enemies:
        enemy.draw(screen)

    game.player.draw(screen)

    for projectile in game.projectiles:
        projectile.draw(screen)

    pygame.display.flip()


def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    player = Player(screen.get_width() / 4, screen.get_height() / 4)
    enemies = pygame.sprite.Group()
    enemies.add(GrapeTower(pos=pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)))
    game = Game(player=player, enemies=enemies, projectiles=pygame.sprite.Group())

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # wipe the last frame
        screen.fill('green')

        # Handle inputs
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] != keys[pygame.K_s] and keys[pygame.K_a] != keys[pygame.K_d]:
            adjust_pythagoras = 0.7071067811865476
        else:
            adjust_pythagoras = 1
        if keys[pygame.K_w]:
            player.rect.y -= player.speed * adjust_pythagoras * dt
        if keys[pygame.K_s]:
            player.rect.y += player.speed * adjust_pythagoras * dt
        if keys[pygame.K_a]:
            player.rect.x -= player.speed * adjust_pythagoras * dt
        if keys[pygame.K_d]:
            player.rect.x += player.speed * adjust_pythagoras * dt

        # Update world
        update(game, time.perf_counter(), dt)

        # Draw the current game state
        draw(game, screen)

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()


if __name__ == '__main__':
    main()
