# Example file showing a circle moving on screen
import json
import time

import pygame
from pygame import Vector2

from common import Game, GrapeTower, GRAPE_TOWER_WIDTH, GRAPE_TOWER_HEIGHT


def update(game: Game, now, dt):
    pass

def draw(game, screen, cursor_mode):

    mouse_pos = Vector2(pygame.mouse.get_pos())

    if cursor_mode == 'grape':
        grape_tower = GrapeTower(pos=Vector2(mouse_pos.x - GRAPE_TOWER_WIDTH / 2, mouse_pos.y - GRAPE_TOWER_HEIGHT /2))
        grape_tower.draw(screen)

    for enemy in game.enemies:
        enemy.draw(screen)

    pygame.display.flip()


def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    # Load the level
    # with open('levels/level01.json') as f:
    #     file_contents = f.read()
    #     level_obj = json.loads(file_contents)
    #     print(level_obj['towers'][1])

    game = Game(player=None, enemies=pygame.sprite.Group(), projectiles=pygame.sprite.Group())
    cursor_mode = None

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = event.pos
                grape_tower = GrapeTower(pos=Vector2(pos[0] - GRAPE_TOWER_WIDTH / 2, pos[1] - GRAPE_TOWER_HEIGHT /2))
                game.enemies.add(grape_tower)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    towers_list = []
                    for enemy in game.enemies:
                        towers_list.append({
                            'type': 'grape',
                            'position': enemy.rect.topleft,
                        })
                    with open('levels/level01.json', 'w') as f:
                        level_obj = {
                            'player_starting_location': [250, 250],
                            'towers': towers_list
                        }
                        json_str = json.dumps(level_obj)
                        f.write(json_str)

        # wipe the last frame
        screen.fill('green')

        # Handle inputs
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            cursor_mode = 'grape'

        # Update world
        update(game, time.perf_counter(), dt)

        # Draw the current game state
        draw(game, screen, cursor_mode)

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()


if __name__ == '__main__':
    main()
