# Example file showing a circle moving on screen
import json
import sys
import time

import pygame
from pygame import Vector2

from common import Game, GrapeTower, PLACEABLE_OBJECT_CLASSES, load_game, NOT_YET_PLACED
from utils import get_next_uncreated_level_filepath


def update(game: Game, now, dt):
    pass


def draw(game, screen, class_of_obj_to_place):
    mouse_pos = Vector2(pygame.mouse.get_pos())

    for surface in game.surfaces:
        surface.fill('#00000000')

    if class_of_obj_to_place:
        pos = class_of_obj_to_place.pos_from_mouse_pos(mouse_pos)
        obj_to_place = class_of_obj_to_place(game=game, pos=pos, placement_mode=NOT_YET_PLACED)
        obj_to_place.draw(game.surfaces)

    for obj in game.game_objects:
        obj.draw(game.surfaces)

    for surface in game.surfaces:
        screen.blit(surface, (0, 0))

    pygame.display.flip()


def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    level_filepath = sys.argv[1] if len(sys.argv) > 1 else None
    # Load the level
    game = load_game(level_filepath)

    class_of_obj_to_place = None

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and class_of_obj_to_place:
                pos = class_of_obj_to_place.pos_from_mouse_pos(Vector2(event.pos))
                class_of_obj_to_place(game=game, pos=pos)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    objects_list = []
                    for obj in game.game_objects:
                        objects_list.append(
                            {
                                'type': obj.name,
                                'position': obj.rect.topleft,
                            }
                        )
                    if level_filepath is None:
                        level_filepath = get_next_uncreated_level_filepath()
                    with open(level_filepath, 'w') as f:
                        level_obj = {'player_starting_location': [250, 250], 'objects': objects_list}
                        json_str = json.dumps(level_obj)
                        f.write(json_str)

        # wipe the last frame
        screen.fill('green')

        # Handle inputs
        keys = pygame.key.get_pressed()
        for idx, key_name in enumerate(range(pygame.K_1, pygame.K_9)):
            if keys[key_name] and idx < len(PLACEABLE_OBJECT_CLASSES):
                class_of_obj_to_place = PLACEABLE_OBJECT_CLASSES[idx]
                break

        # Update world
        update(game, time.perf_counter(), dt)

        # Draw the current game state
        draw(game, screen, class_of_obj_to_place)

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()


if __name__ == '__main__':
    main()
