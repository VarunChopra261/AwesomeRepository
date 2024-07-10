import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()
# create the screen
screen = pygame.display.set_mode((600, 600))  # (width , height)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)
# background image
background = pygame.image.load("spacebackground.jpg")

# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)  # -1 allows us to play the sound on loop

# Player Image
playerImg = pygame.image.load("battleship.png")
playerX = 260
playerY = 538
playerX_change = 0

# Enemy Image
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("space.png"))
    enemyX.append(random.randint(64, 536))
    enemyY.append(random.randint(50, 100))
    enemyX_change.append(0.25)
    enemyY_change.append(20)

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 538
bulletX_change = 0
bulletY_change = 0.8
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# Game over text
game_over_font = pygame.font.Font("freesansbold.ttf", 60)

def game_over_text():
    over_text = game_over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(over_text, (120, 300))


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def iscollision(x1, x2, y1, y2):
    distance = math.sqrt((pow((x1 - x2), 2)) + (pow((y1 - y2), 2)))
    if distance < 25:
        return True
    else:
        return False


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, j):
    screen.blit(enemyImg[j], (x, y))


# Ready - you can't see the bullet on the screen
# Fire - The bullet is currently moving
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y))


# Game loop
running = True
while running:
    # RGB- Red Green Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.8
            elif event.key == pygame.K_RIGHT:
                playerX_change = 0.8
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change
    # Checking for boundaries of spaceship so it doesn't go out of bounds
    if playerX <= 0:
        playerX = 0
    elif playerX >= 536:
        playerX = 536

    for j in range(num_of_enemies):
        if enemyY[j] > 496:
            for k in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[j] += enemyX_change[j]
        if enemyX[j] <= 0:
            enemyX_change[j] = 0.3
            enemyY[j] += enemyY_change[j]
        elif enemyX[j] >= 536:
            enemyX_change[j] = -0.3
            enemyY[j] += enemyY_change[j]
        # Collision
        collision = iscollision(enemyX[j], bulletX, enemyY[j], bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 538
            bullet_state = "ready"
            score_value += 1
            enemyX[j] = random.randint(64, 536)
            enemyY[j] = random.randint(50, 100)
        enemy(enemyX[j], enemyY[j], j)
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        if bulletY < 0:
            bulletY = 538
            bullet_state = "ready"

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()


