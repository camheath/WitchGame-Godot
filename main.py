# TO DO
# ADD ANIMATIONS TO WITCH, FIREBALL, BATS
# SCROLL BACKGROUND
# ADD PICKUPS AND SFX
# ADD BAT SFX

import pygame
import os
from playerfunctions import handle_witch_movement
import spritesheet
import random
pygame.font.init()
pygame.mixer.init()

WITCH_WIDTH = 72
WITCH_HEIGHT = 90
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Witch Game")

FPS = 60
VEL = 5
BAT_VEL = 3
FIREBALL_VEL = 7
MAX_FIREBALLS = 5

WITCH_HIT = pygame.USEREVENT + 1
BAT_HIT = pygame.USEREVENT + 2

YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


FIREBALL_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'curse3.ogg'))
WITCH_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'hurt.ogg'))
MUSIC = pygame.mixer.music.load(os.path.join('Assets', 'prismaticlight.mp3'))

HEALTH_FONT = pygame.font.SysFont('helvetica', 40)

# Load in images
WITCH_IMAGE = pygame.image.load(os.path.join('Assets', 'witch.png'))
FIREBALL_IMAGE = pygame.image.load(os.path.join('Assets', 'fireball.png'))
FIREBALL = pygame.transform.scale(FIREBALL_IMAGE, (11, 7))
SKY = pygame.image.load(os.path.join('Assets', 'sky.png'))
BAT_IMAGE = pygame.image.load(os.path.join('Assets', 'bat.png'))
witch_sprite_sheet = spritesheet.SpriteSheet(WITCH_IMAGE)
bat_sprite_sheet = spritesheet.SpriteSheet(BAT_IMAGE)
fireball_sprite_sheet = spritesheet.SpriteSheet(FIREBALL_IMAGE)

witch_0 = witch_sprite_sheet.get_image(0, 24, 30, 3, BLACK)

# animation list
bat_animation_list = []
animation_steps = 4
last_update = pygame.time.get_ticks()
animation_cooldown = 5
frame = 0
for x in range(animation_steps):
    bat_animation_list.append(bat_sprite_sheet.get_image(x, 30, 32, 2, BLACK))


def draw_window(witch, witch_health, bats, total_score, fireballs, last_update, frame, animation_cooldown, bat_animation_list):
    WIN.blit(SKY, (0,0))
    WIN.blit(witch_0, (witch.x, witch.y))

    for shot in fireballs:
        #ANIMATE LATER
        WIN.blit((fireball_sprite_sheet.get_image(0, 11, 7, 2, BLACK)), shot)

    # CURRENTLY HAVING ISSUES
    for bat in bats:
        WIN.blit(bat_animation_list[frame], bat)
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            frame += 1
        if frame >= len(bat_animation_list):
            frame = 0
        last_update = current_time
        
        

    witch_health_text = HEALTH_FONT.render("Health: " + str(witch_health), 1, WHITE)
    WIN.blit(witch_health_text, (10, 10))

    score = HEALTH_FONT.render("Score: " + str(total_score), 1, WHITE)
    WIN.blit(score, (WIDTH - score.get_width() - 20, 10))

    pygame.display.update()


def bat_movement(bats, BAT_VEL, witch):
    for bat in bats:
        bat.x -= BAT_VEL
        if bat.colliderect(witch):
            pygame.event.post(pygame.event.Event(WITCH_HIT))
            bats.remove(bat)
        elif bat.x + 60 < 0:
            bats.remove(bat)

def handle_fireballs(fireballs, witch, bats, bonus_score, FIREBALL_VEL, WIDTH):
    for shot in fireballs:
        shot.x += FIREBALL_VEL
        for bat in bats:
            if bat.colliderect(shot):
                fireballs.remove(shot)
                bats.remove(bat)
                pygame.event.post(pygame.event.Event(BAT_HIT))             
            
        if shot.x > WIDTH:
            fireballs.remove(shot)


def main():
    witch = pygame.Rect(100, 300, WITCH_WIDTH, WITCH_HEIGHT)
    fireballs = []
    bats = []
    witch_health = 5
    time_score = 0
    timer = 0
    bonus_score = 0
    total_score = 0

    pygame.mixer.music.set_volume(.5)
    pygame.mixer.music.play(loops = -1)

    clock = pygame.time.Clock()
    run = True
    while run:    
        clock.tick(FPS)
        
        timer += 1
        if timer % 60 == 0:
            time_score += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN and len(fireballs) < MAX_FIREBALLS:
                # ANIMATE LATER
                if event.key == pygame.K_SPACE:
                    shot = pygame.Rect(witch.x + witch.width, witch.y + witch.height//2 - 2, 10, 5)
                    fireballs.append(shot)
                    FIREBALL_FIRE_SOUND.play()

            if event.type == WITCH_HIT:
                witch_health -= 1
                WITCH_HIT_SOUND.play()

            if event.type == BAT_HIT:
                bonus_score += 10

        # BAT SPAWNING
        if timer < 25:
            if timer % 120 == 0:
                spawn_point = random.randint(10 , HEIGHT - 65)
                for bat in bats:
                    if bat.y == spawn_point:
                        spawn_point = random.randint(10, HEIGHT - 65)
                bat = pygame.Rect(WIDTH + 5, spawn_point, 60, 64)
                bats.append(bat)
        elif timer < 60:
            if timer % 100 == 0:
                spawn_point = random.randint(10, HEIGHT - 65)
                for bat in bats:
                    if bat.y == spawn_point:
                        spawn_point = random.randint(10, HEIGHT - 65)
                bat = pygame.Rect(WIDTH + 5, spawn_point, 60, 64)
                bats.append(bat)
        else:
            if timer % 80 == 0:
                spawn_point = random.randint(10, HEIGHT - 65)
                for bat in bats:
                    if bat.y == spawn_point:
                        spawn_point = random.randint(10, HEIGHT - 65)
                bat = pygame.Rect(WIDTH + 5, spawn_point, 60, 64)
                bats.append(bat)


        keys_pressed = pygame.key.get_pressed()
        handle_witch_movement(keys_pressed, witch, VEL, WIDTH, HEIGHT)
        handle_fireballs(fireballs, witch, bats, bonus_score, FIREBALL_VEL, WIDTH)
        bat_movement(bats, BAT_VEL, witch)

        total_score = time_score + bonus_score

        if witch_health <= 0:
            draw_window(witch, witch_health, bats, total_score, fireballs, last_update, frame, animation_cooldown, bat_animation_list)
            break

        draw_window(witch, witch_health, bats, total_score, fireballs, last_update, frame, animation_cooldown, bat_animation_list)
    

    draw_text = HEALTH_FONT.render("FINAL SCORE: " + str(total_score), 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()  
    pygame.time.delay(5000)

    pygame.quit()

if __name__ == "__main__":
    main()
