# TO DO
# ADD ANIMATIONS TO WITCH

import pygame
import os
from playerfunctions import handle_witch_movement
import spritesheet
import random
import sys
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
ORB_VEL = 1
FIREBALL_VEL = 7
MAX_FIREBALLS = 5

WITCH_HIT = pygame.USEREVENT + 1
BAT_HIT = pygame.USEREVENT + 2
ORB_PICKUP = pygame.USEREVENT + 3
BREAD_PICKUP = pygame.USEREVENT + 4

YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 120)



HEALTH_FONT = pygame.font.SysFont('helvetica', 40)


def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Load in audio
# Load urls
MUSIC_URL = resource_path('Assets\prismaticlight.mp3')
FIREBALL_FIRE_URL = resource_path('Assets\curse3.ogg')
WITCH_HIT_URL = resource_path('Assets\hurt.ogg')
BAT_HIT_URL = resource_path('Assets\hit.ogg')
ORB_PICKUP_URL = resource_path('Assets\coin.ogg')
BREAD_PICKUP_URL = resource_path('Assets\heal.ogg')

FIREBALL_FIRE_SOUND = pygame.mixer.Sound(FIREBALL_FIRE_URL)
WITCH_HIT_SOUND = pygame.mixer.Sound(WITCH_HIT_URL)
BAT_HIT_SOUND = pygame.mixer.Sound(BAT_HIT_URL)
ORB_PICKUP_SOUND = pygame.mixer.Sound(ORB_PICKUP_URL)
BREAD_PICKUP_SOUND = pygame.mixer.Sound(BREAD_PICKUP_URL)
MUSIC = pygame.mixer.music.load(MUSIC_URL)

# Load in images
# Load urls
WITCH_URL = resource_path('Assets/witch.png')
FIREBALL_URL = resource_path('Assets/fireball.png')
ORB_URL = resource_path('Assets/yellow_orb.png')
SKY_URL = resource_path('Assets/sky.png')
SNOW_URL = resource_path('Assets/snow.png')    
BAT_URL = resource_path('Assets/bat.png')
BREAD_URL = resource_path('Assets/bread.png')


WITCH_IMAGE = pygame.image.load(WITCH_URL)

FIREBALL_IMAGE = pygame.image.load(FIREBALL_URL) 
FIREBALL = pygame.transform.scale(FIREBALL_IMAGE, (11, 7))

ORB_IMAGE = pygame.image.load(ORB_URL)

SKY_IMAGE = pygame.image.load(SKY_URL)
SKY = pygame.transform.scale(SKY_IMAGE, (448, HEIGHT))

SNOW_IMAGE = pygame.image.load(SNOW_URL)
SNOW = pygame.transform.scale(SNOW_IMAGE, (WIDTH, HEIGHT))

BAT_IMAGE = pygame.image.load(BAT_URL)

BREAD_IMAGE = pygame.image.load(BREAD_URL)
BREAD = pygame.transform.scale(BREAD_IMAGE, (46, 46))

# Spritesheets
witch_sprite_sheet = spritesheet.SpriteSheet(WITCH_IMAGE)
bat_sprite_sheet = spritesheet.SpriteSheet(BAT_IMAGE)
fireball_sprite_sheet = spritesheet.SpriteSheet(FIREBALL_IMAGE)
orb_sprite_sheet = spritesheet.SpriteSheet(ORB_IMAGE)
witch_0 = witch_sprite_sheet.get_image(0, 24, 30, 3, BLACK)




def draw_window(witch, witch_health, bats, total_score, fireballs, orbs, bread_list, sky_scroll, snow_scroll, timer, bat_frame, orb_frame):
    for x in range(4):
        WIN.blit(SKY, (x * 448 + sky_scroll, 0))

    WIN.blit(witch_0, (witch.x, witch.y))

    for shot in fireballs:
        WIN.blit(fireball_sprite_sheet.get_image(0, 11, 7, 2, BLACK), shot)

    for orb in orbs:
        WIN.blit(orb_sprite_sheet.get_image(orb_frame, 32, 32, 2, BLACK), orb)

    for bread in bread_list:
        WIN.blit(BREAD, bread)

    for bat in bats:
        WIN.blit(bat_sprite_sheet.get_image(bat_frame, 30, 32, 2, BLACK), bat)
        

    for y in range(4):
        WIN.blit(SNOW, (0, -y * HEIGHT + snow_scroll))


    witch_health_text = HEALTH_FONT.render("Health: " + str(witch_health), 1, RED)
    WIN.blit(witch_health_text, (10, 10))

    score = HEALTH_FONT.render("Score: " + str(total_score), 1, RED)
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


def orb_movement(orbs, ORB_VEL, witch):
    for orb in orbs:
        orb.x -= ORB_VEL
        if orb.colliderect(witch):
            pygame.event.post(pygame.event.Event(ORB_PICKUP))
            orbs.remove(orb)
        elif orb.x + 32 < 0:
            orbs.remove(orb)

def bread_movement(bread_list, ORB_VEL, witch):
    for bread in bread_list:
        bread.x -= ORB_VEL
        if bread.colliderect(witch):
            pygame.event.post(pygame.event.Event(BREAD_PICKUP))
            bread_list.remove(bread)
        elif bread.x + 46 < 0:
            bread_list.remove(bread)


def main():
    witch = pygame.Rect(100, 300, WITCH_WIDTH, WITCH_HEIGHT)
    fireballs = []
    bats = []
    witch_health = 5
    time_score = 0
    timer = 0
    bonus_score = 0
    total_score = 0
    orbs = []
    bread_list = []
    sky_scroll = 0
    snow_scroll = 0
    bat_frame = 0
    orb_frame = 0

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
                    shot = pygame.Rect(witch.x + witch.width, witch.y + witch.height//2 - 2, 22, 14)
                    fireballs.append(shot)
                    FIREBALL_FIRE_SOUND.play()

            if event.type == WITCH_HIT:
                witch_health -= 1
                WITCH_HIT_SOUND.play()

            if event.type == BAT_HIT:
                bonus_score += 10
                BAT_HIT_SOUND.play()

            if event.type == ORB_PICKUP:
                bonus_score += 300
                ORB_PICKUP_SOUND.play()

            if event.type == BREAD_PICKUP:
                witch_health += 1
                BREAD_PICKUP_SOUND.play()


        # BAT SPAWNING
        if timer < 500:
            if timer % 120 == 0:
                spawn_point = random.randint(10 , HEIGHT - 65)
                for bat in bats:
                    if bat.y == spawn_point:
                        spawn_point = random.randint(10, HEIGHT - 65)
                bat = pygame.Rect(WIDTH + 5, spawn_point, 60, 64)
                bats.append(bat)
        elif timer < 1200:
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

        # ANIMATE BATS       
        if timer % 10 == 0:
            bat_frame += 1
            if bat_frame >= 5:
                bat_frame = 0

        # ANIMATE ORBS       
        if timer % 5 == 0:
            orb_frame += 1
            if orb_frame >= 4:
                orb_frame = 0

        orb_chance = random.randint(0, 200)
        if orb_chance == 0 and len(orbs) == 0 and timer > 500:
            spawn_point = random.randint(10 , HEIGHT - 65)
            orb = pygame.Rect(WIDTH + 5, spawn_point, 64, 64)
            orbs.append(orb)

        bread_chance = random.randint(0, 800)
        if bread_chance == 0 and len(bread_list) == 0 and timer > 600 and witch_health < 5:
            spawn_point = random.randint(10 , HEIGHT - 65)
            bread = pygame.Rect(WIDTH + 5, spawn_point, 46, 46)
            bread_list.append(bread)


        keys_pressed = pygame.key.get_pressed()
        handle_witch_movement(keys_pressed, witch, VEL, WIDTH, HEIGHT)
        handle_fireballs(fireballs, witch, bats, bonus_score, FIREBALL_VEL, WIDTH)
        bat_movement(bats, BAT_VEL, witch)
        orb_movement(orbs, ORB_VEL, witch)
        bread_movement(bread_list, ORB_VEL, witch)

        sky_scroll -= .5
        snow_scroll += 1

        if abs(sky_scroll) > 446:
            sky_scroll = 0
        
        if abs(snow_scroll) > HEIGHT:
            snow_scroll = 0
        

        total_score = time_score + bonus_score

        if witch_health <= 0:
            draw_window(witch, witch_health, bats, total_score, fireballs, orbs, bread_list, sky_scroll, snow_scroll, timer, bat_frame, orb_frame)
            break

            
        draw_window(witch, witch_health, bats, total_score, fireballs, orbs, bread_list, sky_scroll, snow_scroll, timer, bat_frame, orb_frame)

    

    draw_text = HEALTH_FONT.render("FINAL SCORE: " + str(total_score), 1, RED)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()  
    pygame.time.delay(5000)

    pygame.quit()

if __name__ == "__main__":
    main()
