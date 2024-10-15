# Example file showing a circle moving on screen
import json
import time

import pygame

from common import Game, Player, GrapeTower


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
        enemy.draw_range(screen)

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

    # Load the level
    with open('levels/level01.json') as f:
        file_contents = f.read()
        level_obj = json.loads(file_contents)
        print(level_obj['towers'][1])


    player = Player(level_obj['player_starting_location'][0], level_obj['player_starting_location'][1])
    enemies = pygame.sprite.Group()
    for tower in level_obj['towers']:
        if tower['type'] == 'grape':
            enemies.add(GrapeTower(pos=pygame.Vector2(tower['position'][0], tower['position'][1])))
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
