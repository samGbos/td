For those interested in the coding part of the game, here are some questions/challenges to check your understanding of the code.

You can run the code for each question with `uv run learning/q1.py` etc.

1. Here is some code for updating the player's position based on the W,A,S, and D keys: 

```
    if keys[pygame.K_w]:
        player_pos.y -= player_speed * dt
    if keys[pygame.K_s]:
        player_pos.y += player_speed * dt
    if keys[pygame.K_a]:
        player_pos.x -= player_speed * dt
    if keys[pygame.K_d]:
        player_pos.x += player_speed * dt
```

What's "incorrect" about that code? (The code runs fine, but behaves differently than most users would expect).

How would you fix it?

2. q2.py removes the `* dt` part of the above lines:

```
    if keys[pygame.K_w]:
        player_pos.y -= player_speed
    if keys[pygame.K_s]:
        player_pos.y += player_speed
    if keys[pygame.K_a]:
        player_pos.x -= player_speed
    if keys[pygame.K_d]:
        player_pos.x += player_speed
```

and changed the player_speed variable accordingly. What's a potential problem with the changed code?

3. Challenge: Add a piece of text somewhere on the screen that shows the current number of frames per second.
(An easier version is to just print the frames per second on every iteration of the game loop.)

