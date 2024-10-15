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

GRAPE_TOWER_RANGE = 300
GRAPE_TOWER_WIDTH = 64
GRAPE_TOWER_HEIGHT = 64

class GrapeTower(pygame.sprite.Sprite):
    last_fired: float | None = None

    def __init__(self, pos: Vector2):
        super().__init__()
        self.image = pygame.Surface([GRAPE_TOWER_WIDTH, GRAPE_TOWER_HEIGHT])
        self.image.fill('red')
        self.rect = pygame.rect.Rect(pos.x, pos.y, self.image.get_width(), self.image.get_height())

    def update(self, game, now, _dt):
        dir_x = game.player.rect.center[0] - self.rect.center[0]
        dir_y = game.player.rect.center[1] - self.rect.center[1]
        direction = pygame.Vector2(dir_x, dir_y)
        dist_from_player = direction.length()
        if dist_from_player <= GRAPE_TOWER_RANGE and (self.last_fired is None or now > self.last_fired + 1):
            if direction.length_squared():
                direction.normalize_ip()
            game.projectiles.add(Grape(pos=Vector2(self.rect.center), velocity=direction * 500))
            self.last_fired = now

    def draw_range(self, screen):
        surface = pygame.Surface((GRAPE_TOWER_RANGE * 2, GRAPE_TOWER_RANGE * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, '#0000ff55', (GRAPE_TOWER_RANGE, GRAPE_TOWER_RANGE), GRAPE_TOWER_RANGE)
        screen.blit(surface, (self.rect.center[0] - GRAPE_TOWER_RANGE, self.rect.center[1] - GRAPE_TOWER_RANGE))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Grape(pygame.sprite.Sprite):
    def __init__(self, pos: Vector2, velocity: Vector2):
        super().__init__()
        self.image = pygame.Surface([8, 8])
        self.image.fill('black')

        self.rect = pygame.rect.Rect(pos.x, pos.y, self.image.get_width(), self.image.get_height())
        self.starting_pos = pos

        self.velocity = velocity
        self.pending_removal = False

    def update(self, game, _now, dt):

        dir_x = self.starting_pos.x - self.rect.center[0]
        dir_y = self.starting_pos.y - self.rect.center[1]
        direction = pygame.Vector2(dir_x, dir_y)
        dist_from_starting_pos = direction.length()
        if self.pending_removal or is_offscreen(self.rect) or self.velocity.length_squared() == 0 or dist_from_starting_pos > GRAPE_TOWER_RANGE:
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
