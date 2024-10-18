import json
from dataclasses import dataclass

import pygame
from pygame import Vector2

GAME_WIDTH = 1280
GAME_HEIGHT = 720

GRAPE_TOWER_RANGE = 300
GRAPE_TOWER_WIDTH = 64
GRAPE_TOWER_HEIGHT = 64

KIWI_TOWER_RANGE = 200
KIWI_TOWER_WIDTH = 64
KIWI_TOWER_HEIGHT = 64

DRAGON_FRUIT_TOWER_RANGE = 250
DRAGON_FRUIT_TOWER_WIDTH = 32
DRAGON_FRUIT_TOWER_HEIGHT = 32

DEFAULT_PLAYER_START_X = GAME_WIDTH / 4
DEFAULT_PLAYER_START_Y = GAME_HEIGHT / 4

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
    name = 'grape'

    def __init__(self, pos: Vector2):
        super().__init__()
        self.image = pygame.Surface([GRAPE_TOWER_WIDTH, GRAPE_TOWER_HEIGHT])
        self.image.fill('red')
        self.rect = pygame.rect.Rect(pos.x, pos.y, self.image.get_width(), self.image.get_height())
        self.last_fired: float | None = None

    @staticmethod
    def pos_from_mouse_pos(mouse_pos):
        return Vector2(mouse_pos.x - GRAPE_TOWER_WIDTH / 2, mouse_pos.y - GRAPE_TOWER_HEIGHT / 2)

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

        self.pos = pos
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
        self.pos += dpos
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class KiwiTower(pygame.sprite.Sprite):
    name = "kiwi"
    def __init__(self, pos: Vector2):
        super().__init__()
        self.image = pygame.Surface([KIWI_TOWER_WIDTH, KIWI_TOWER_HEIGHT])
        self.image.fill('blue')
        self.rect = pygame.rect.Rect(pos.x, pos.y, self.image.get_width(), self.image.get_height())
        self.last_fired: float | None = None
    @staticmethod
    def pos_from_mouse_pos(mouse_pos):
        return Vector2(mouse_pos.x - KIWI_TOWER_WIDTH / 2, mouse_pos.y - KIWI_TOWER_HEIGHT / 2)

    def update(self, game, now, _dt):
        dir_x = game.player.rect.center[0] - self.rect.center[0]
        dir_y = game.player.rect.center[1] - self.rect.center[1]
        direction = pygame.Vector2(dir_x, dir_y)
        dist_from_player = direction.length()
        if dist_from_player <= KIWI_TOWER_RANGE and (self.last_fired is None or now > self.last_fired + 0.1):
            if direction.length_squared():
                direction.normalize_ip()
            game.projectiles.add(Kiwi(pos=Vector2(self.rect.center), velocity=direction * 100))
            self.last_fired = now

    def draw_range(self, screen):
        surface = pygame.Surface((KIWI_TOWER_RANGE * 2, KIWI_TOWER_RANGE * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, '#0000ff55', (KIWI_TOWER_RANGE, KIWI_TOWER_RANGE), KIWI_TOWER_RANGE)
        screen.blit(surface, (self.rect.center[0] - KIWI_TOWER_RANGE, self.rect.center[1] - KIWI_TOWER_RANGE))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Kiwi(pygame.sprite.Sprite):
    def __init__(self, pos: Vector2, velocity: Vector2):
        super().__init__()
        self.image = pygame.Surface([16, 16])
        self.image.fill('black')

        self.pos = pos
        self.rect = pygame.rect.Rect(pos.x, pos.y, self.image.get_width(), self.image.get_height())
        self.starting_pos = pos

        self.velocity = velocity
        self.pending_removal = False

    def update(self, game, _now, dt):

        dir_x = self.starting_pos.x - self.rect.center[0]
        dir_y = self.starting_pos.y - self.rect.center[1]
        direction = pygame.Vector2(dir_x, dir_y)
        dist_from_starting_pos = direction.length()
        if self.pending_removal or is_offscreen(self.rect) or self.velocity.length_squared() == 0 or dist_from_starting_pos > KIWI_TOWER_RANGE:
            self.kill()
            return

        dpos = self.velocity * dt
        self.pos += dpos
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class DragonFruitTower(pygame.sprite.Sprite):
    name = 'dragonfruit'

    def __init__(self, pos: Vector2):
        super().__init__()
        self.image = pygame.Surface([DRAGON_FRUIT_TOWER_WIDTH, DRAGON_FRUIT_TOWER_HEIGHT])
        self.image.fill('orange')
        self.rect = pygame.rect.Rect(pos.x, pos.y, self.image.get_width(), self.image.get_height())
        self.last_fired: float | None = None

    @staticmethod
    def pos_from_mouse_pos(mouse_pos):
        return Vector2(mouse_pos.x - DRAGON_FRUIT_TOWER_WIDTH / 2, mouse_pos.y - DRAGON_FRUIT_TOWER_HEIGHT / 2)

    def update(self, game, now, _dt):
        dir_x = game.player.rect.center[0] - self.rect.center[0]
        dir_y = game.player.rect.center[1] - self.rect.center[1]
        direction = pygame.Vector2(dir_x, dir_y)
        dist_from_player = direction.length()
        if dist_from_player <= DRAGON_FRUIT_TOWER_RANGE and (self.last_fired is None or now > self.last_fired + 2):
            if direction.length_squared():
                direction.normalize_ip()
                speedofdiffbullets = 300 
                for i in range(3): #this should make 3 bullets right? why are only 2 being shown?
                    game.projectiles.add(Grape(pos=Vector2(self.rect.center), velocity=direction * speedofdiffbullets))
                    speedofdiffbullets -= 50 #decrementing speed of var speedofdiffbullets
                self.last_fired = now

    def draw_range(self, screen):
        surface = pygame.Surface((DRAGON_FRUIT_TOWER_RANGE * 2, DRAGON_FRUIT_TOWER_RANGE * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, '#0000ff55', (DRAGON_FRUIT_TOWER_RANGE, DRAGON_FRUIT_TOWER_RANGE), DRAGON_FRUIT_TOWER_RANGE)
        screen.blit(surface, (self.rect.center[0] - DRAGON_FRUIT_TOWER_RANGE, self.rect.center[1] - DRAGON_FRUIT_TOWER_RANGE))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class DragonFruit(pygame.sprite.Sprite):
    def __init__(self, pos: Vector2, velocity: Vector2):
        super().__init__()
        self.image = pygame.Surface([8, 8])
        self.image.fill('black')

        self.pos = pos
        self.rect = pygame.rect.Rect(pos.x, pos.y, self.image.get_width(), self.image.get_height())
        self.starting_pos = pos

        self.velocity = velocity
        self.pending_removal = False

    def update(self, game, _now, dt):

        dir_x = self.starting_pos.x - self.rect.center[0]
        dir_y = self.starting_pos.y - self.rect.center[1]
        direction = pygame.Vector2(dir_x, dir_y)
        dist_from_starting_pos = direction.length()
        if self.pending_removal or is_offscreen(self.rect) or self.velocity.length_squared() == 0 or dist_from_starting_pos > DRAGON_FRUIT_TOWER_RANGE:
            self.kill()
            return

        dpos = self.velocity * dt
        self.pos += dpos
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

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

TOWER_CLASSES = [GrapeTower, KiwiTower, DragonFruitTower]

def load_game(filepath):
    if filepath:
        print(f"Loading {filepath}")
    else:
        print("Loading new level")
    enemies = pygame.sprite.Group()

    if filepath:
        with open(filepath) as f:
            file_contents = f.read()
            level_obj = json.loads(file_contents)
            player = Player(level_obj['player_starting_location'][0], level_obj['player_starting_location'][1])
            for tower in level_obj['towers']:
                for tower_cls in TOWER_CLASSES:
                    if tower_cls.name == tower['type']:
                        enemies.add(tower_cls(pos=pygame.Vector2(tower['position'][0], tower['position'][1])))

    else:
        player = Player(DEFAULT_PLAYER_START_X, DEFAULT_PLAYER_START_Y)

    game = Game(player=player, enemies=enemies, projectiles=pygame.sprite.Group())
    return game


@dataclass
class Game:
    player: Player
    enemies: pygame.sprite.Group
    projectiles: pygame.sprite.Group


