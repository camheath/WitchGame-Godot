import pygame
import os
from playerfunctions import handle_witch_movement, handle_fireballs
pygame.font.init()
pygame.mixer.init()

WITCH_WIDTH = 100
WITCH_HEIGHT = 100
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Witch Game")

FPS = 60
VEL = 5
FIREBALL_VEL = 7
MAX_FIREBALLS = 3

WITCH_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)


BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('helvetica', 40)


# Load in images
WITCH_IMAGE = pygame.image.load(os.path.join('Assets', 'witch.png'))
WITCH = pygame.transform.scale(WITCH_IMAGE, (WITCH_WIDTH, WITCH_HEIGHT))
FIREBALL_IMAGE = pygame.image.load(os.path.join('Assets', 'fireball.png'))
FIREBALL = pygame.transform.scale(FIREBALL_IMAGE, (11, 7))
SKY = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'sky.png')), (WIDTH, HEIGHT))


def draw_window(witch, witch_health, time_score, fireballs):
    WIN.blit(SKY, (0,0))
    WIN.blit(WITCH, (witch.x, witch.y))
    
    for shot in fireballs:
        pygame.draw.rect(WIN, YELLOW, shot)

    witch_health_text = HEALTH_FONT.render("Health: " + str(witch_health), 1, WHITE)
    WIN.blit(witch_health_text, (10, 10))

    score = HEALTH_FONT.render("Score: " + str(time_score), 1, WHITE)
    WIN.blit(score, (WIDTH - score.get_width() - 20, 10))

    pygame.display.update()



def main():
    witch = pygame.Rect(100, 300, WITCH_WIDTH, WITCH_HEIGHT)
    fireballs = []
    witch_health = 5
    time_score = 0
    timer = 0
    bonus_score = 0

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
                
            if event.type == pygame.KEYDOWN and len(fireballs) < MAX_FIREBALLS:
                if event.key == pygame.K_SPACE:
                    shot = pygame.Rect(witch.x + witch.width, witch.y + witch.height//2 - 2, 10, 5)
                    fireballs.append(shot)
                    BULLET_FIRE_SOUND.play()

            if event.type == WITCH_HIT:
                witch_health -= 1
                BULLET_HIT_SOUND.play()


        keys_pressed = pygame.key.get_pressed()
        handle_witch_movement(keys_pressed, witch, VEL, WIDTH, HEIGHT)
        handle_fireballs(fireballs, witch, FIREBALL_VEL, WIDTH)

        draw_window(witch, witch_health, time_score, fireballs)
    
    pygame.quit()


if __name__ == "__main__":
    main()
