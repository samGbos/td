# Example file showing a circle moving on screen
import sys
import time

import pygame

from common import Game, load_game
from utils import get_latest_level_filepath_and_number


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


    for surface in game.surfaces:
        surface.fill('#00000000')

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

    # Load the level
    level_filepath = sys.argv[1] if len(sys.argv) > 1 else get_latest_level_filepath_and_number()[0]
    game = load_game(level_filepath)

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

        # Move up/down
        if keys[pygame.K_w] or keys[pygame.K_s]:
            if keys[pygame.K_w]:
                game.player.rect.y -= game.player.speed * adjust_pythagoras * dt
            if keys[pygame.K_s]:
                game.player.rect.y += game.player.speed * adjust_pythagoras * dt

            blocking_objs = pygame.sprite.spritecollide(game.player, game.blockers, False)
            for blocking_obj in blocking_objs:
                if keys[pygame.K_w]:
                    game.player.rect.top = blocking_obj.rect.bottom
                if keys[pygame.K_s]:
                    game.player.rect.bottom = blocking_obj.rect.top

        # Move left/right
        if keys[pygame.K_a] or keys[pygame.K_d]:
            if keys[pygame.K_a]:
                game.player.rect.x -= game.player.speed * adjust_pythagoras * dt
            if keys[pygame.K_d]:
                game.player.rect.x += game.player.speed * adjust_pythagoras * dt

            blocking_objs = pygame.sprite.spritecollide(game.player, game.blockers, False)
            for blocking_obj in blocking_objs:
                if keys[pygame.K_a]:
                    game.player.rect.left = blocking_obj.rect.right
                if keys[pygame.K_d]:
                    game.player.rect.right = blocking_obj.rect.left

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
