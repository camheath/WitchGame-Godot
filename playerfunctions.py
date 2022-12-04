import pygame

def handle_witch_movement(keys_pressed, witch, VEL, WIDTH, HEIGHT):
    if keys_pressed[pygame.K_a] and witch.x - VEL or keys_pressed[pygame.K_LEFT] and witch.x - VEL > 0: # LEFT
        witch.x -= VEL
    if keys_pressed[pygame.K_d] and witch.x + VEL + witch.width or keys_pressed[pygame.K_RIGHT] and witch.x + VEL + witch.width < WIDTH: # RIGHT
        witch.x += VEL
    if keys_pressed[pygame.K_w] and witch.y - VEL > 0 or keys_pressed[pygame.K_UP] and witch.y - VEL > 0: # UP
        witch.y -= VEL
    if keys_pressed[pygame.K_s] and witch.y + VEL + witch.height < HEIGHT - 15 or keys_pressed[pygame.K_DOWN] and witch.y + VEL + witch.height < HEIGHT - 15: # DOWN
        witch.y += VEL


def handle_fireballs(fireballs, witch, FIREBALL_VEL, WIDTH):
    for shot in fireballs:
        shot.x += FIREBALL_VEL
#        if red.colliderect(bullet):
#            pygame.event.post(pygame.event.Event(RED_HIT))
#            yellow_bullets.remove(bullet)
        if shot.x > WIDTH:
            fireballs.remove(shot)