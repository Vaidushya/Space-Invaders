import pygame
import random
import math

# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
PLAYER_START_X = 370
PLAYER_START_Y = 380
ENEMY_START_Y_MIN = 50
ENEMY_START_Y_MAX = 150
ENEMY_SPEED_X = 4
ENEMY_SPEED_Y = 40
BULLET_SPEED_Y = 10
COLLISION_DISTANCE = 27

# initialize pygame
pygame.init()

# screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pygame.image.load("space_bg.png")

# caption
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# player
player_img = pygame.image.load("space_ship.png")
player_x = PLAYER_START_X
player_y = PLAYER_START_Y
player_x_change = 0

# enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
no_of_enemy = 6

for i in range(no_of_enemy):
    enemy_img.append(pygame.image.load("enemy.png"))
    enemy_x.append(random.randint(0, SCREEN_WIDTH - 64))
    enemy_y.append(random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX))
    enemy_x_change.append(ENEMY_SPEED_X)
    enemy_y_change.append(ENEMY_SPEED_Y)

# bullet
bullet_img = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = PLAYER_START_Y
Bullet_x_change = 0
bullet_y_change = BULLET_SPEED_Y
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# game over text
over_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    
def player(x ,y):
    screen.blit(player_img, (x ,y))

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

def iscollision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2)
    return distance < COLLISION_DISTANCE

# game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)
        if event.key == pygame.K_UP and event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
            player_x_change = 0

        # player movement
        player_x += player_x_change
        player_x = max(0, min(player_x, SCREEN_WIDTH - 64))

        # enemy movement
        for i in range(no_of_enemy):
            if enemy_y[i] > 340:
                for j in range(no_of_enemy):
                   enemy_y[j] = 2000
                game_over_text()
                break
        
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0 or enemy_x[i] >= SCREEN_WIDTH - 64:
            enemy_x_change[i] *= -1
            enemy_y[i] += enemy_y_change[i]

        # Collision Check
        if iscollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
            bullet_y = PLAYER_START_Y
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, SCREEN_WIDTH - 64)
            enemy_y[i] = random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX)

        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet Movement
    if bullet_y <= 0:
        bullet_y = PLAYER_START_Y
        bullet_state = "ready"
    elif bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()