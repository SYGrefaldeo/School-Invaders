import random
import math
import pygame
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load("assets/blackboard.png")
mixer.music.load("audio/background.wav")
mixer.music.play(-1)

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("assets/logo.png")
pygame.display.set_icon(icon)

Char = pygame.image.load("assets/char.png")
playerX = 370
playerY = 480
playerX_change = 0

Enemy = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 9

for i in range(num_of_enemies):
    Enemy.append(pygame.image.load("assets/assignments.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(3)
    enemyY_change.append(30)

Bullet = pygame.image.load("assets/pencil.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)

restart = pygame.font.Font('freesansbold.ttf', 30)



def show_score(x,y):
    score = font.render("Score : " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text= over_font.render("GAME OVER ", True, (255,255,255))
    screen.blit(over_text, (200, 250))

def reset():
    reset_text= restart.render("Restart ", True, (255,255,255))
    screen.blit(reset_text, (200, 350))

def player(x,y) :
    screen.blit(Char, (x, y))

def enemy(x, y, i) :
    screen.blit(Enemy[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(Bullet, (x + 16, y + 10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -3.5
            if event.key == pygame.K_d:
                playerX_change = 3.5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound("audio/laser (1).wav")
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or pygame.K_a:
                playerX_change = 0



    screen.fill((0, 0, 0))
    screen.blit(background, (0,0))
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    for i in range(num_of_enemies):

        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            reset()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound("audio/explosion (1).wav")
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)


    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change



    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
