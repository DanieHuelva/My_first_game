import random
import pygame
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((900, 506))

pygame.display.set_caption("Test out your rizz")

background = pygame.image.load('bg-game.jpg')

mixer.music.load('bg-music.mp3')
mixer.music.play(-1)

score = 0
speed = 0

def scoring(score):
    if score < 5:
        speed = 1
    elif score < 10:
        speed = 1.5
    elif score < 15:
        speed = 1.8
    elif score < 20:
        speed = 2
    elif score <30:
        speed = 2.3
    else:
        speed = 2.8
    return speed



#The blowing kiss
kiss = pygame.image.load('kiss.png')
kissX = 0
kissY = 390
kiss_changeX = 0
kiss_changeY = 1.3
kiss_state = 'ready'

# Player
playerImg = pygame.image.load('player.png')
playerX = 420
playerY = 390

#Enemy
enemyIMG = []
enemyX = []
enemyY = []
enemy_changeX = []
num_enemies = 6 + scoring(score) * 3 // 2

#poop
loseIMG = []
poop_changes = []
poopX = []
poopY = []

#fonts
font = pygame.font.Font('freesansbold.ttf', 40)
over_font = pygame.font.Font('Gameplay.ttf', 70)
additional = pygame.font.Font('Gameplay.ttf', 25)


for _ in range(num_enemies):
    enemyIMG.append(pygame.image.load('walking.png'))
    gen_x = random.randint(50,620)
    gen_y = random.randint(40, 280)
    enemyX.append(gen_x)
    enemyY.append(gen_y)
    poopX.append(gen_x)
    poopY.append(gen_y)
    enemy_changeX.append(0.4)
    loseIMG.append(pygame.image.load('poop.png'))
    poop_changes.append(0.2)



def myPlayer(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, e):
    screen.blit(enemyIMG[e], (x, y))


def lose(x, y, e):
    screen.blit(loseIMG[e], (x, y))
    y += enemy_changeX[e]


# blowing the kiss
def rizzing(x, y):
    global kiss_state
    kiss_state = 'blow'
    screen.blit(kiss, (x, y))


# This is gonna be when the kiss hits the guy
def collide(enemyX, enemyY, kissX, kissY,):
    distance = math.sqrt((math.pow((enemyX + 20) - kissX, 2)) + (math.pow(enemyY - kissY, 2)))
    if distance < 30:
        return True
    else:
        return False


def player_score():
    show_score = font.render('Score: ' + str(score), True, (235, 99, 180))
    screen.blit(show_score, (350, 470))


def gameOver(poopX, poopY, playerX, playerY):
    distance = math.sqrt((math.pow(poopX-20 - playerX, 2)) + (math.pow((poopY-20) - playerY, 2)))
    if distance < 30:
        return True
    else:
        return False


def game_over_text():
    game_is_over = over_font.render('GAME OVER', True, (235, 99, 180))
    screen.blit(game_is_over, (230, 160))


def add_text():
    if score < 5:
        game_is_over = additional.render('eww you got no games!!', True, (235, 99, 180))
    elif score < 10:
        game_is_over = additional.render('Please be better', True, (235, 99, 180))
    elif score < 20:
        game_is_over = additional.render('Hmm a pretty decent rizz', True, (235, 99, 180))
    elif score < 30:
        game_is_over = additional.render('What an effin rizzler right there', True, (235, 99, 180))
    else:
        game_is_over = additional.render('Yo mama raised you right', True, (235, 99, 180))
    screen.blit(game_is_over, (230, 280))

xChange = 0
# The game
running = True
while running:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:  # pressing keyboard
            if event.key == pygame.K_LEFT:
                xChange = -2
            if event.key == pygame.K_RIGHT:
                xChange = 2
            if event.key == pygame.K_SPACE:
                if kiss_state == "ready":
                    rizzing(playerX, kissY)
                    kissX = playerX
        if event.type == pygame.KEYUP:  # releasing keyboard
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                xChange = 0
    playerX += xChange  # movement of the girl
    kiss_speed = scoring(score)
    changes = 20
    for e in range(num_enemies):
        game_over = gameOver(poopX[e], poopY[e], playerX, playerY)
        if game_over:
            for all in range(num_enemies):
                enemyY[all] = 1000
                poopY[all] = 1000
            break
        enemyX[e] += enemy_changeX[e]
        if enemyX[e] >= 730:
            enemy_changeX[e] = -0.2 - kiss_speed
        elif enemyX[e] <= 50:
            enemy_changeX[e] = 0.2 + kiss_speed
        collision = collide(enemyX[e], enemyY[e], kissX, kissY)
        if collision:
            kissY = 390
            kiss_state = 'ready'
            score += 1
            enemyX[e] = random.randint(50, 710)
            enemyY[e] = random.randint(50, 280)
        poopY[e] += (0.6 + poop_changes[e] * math.pow(kiss_speed, 2) )
        if poopY[e] >= 430:
            poopY[e] = enemyY[e]+30
            poopX[e] = enemyX[e]+10
        lose(poopX[e], poopY[e], e)
        enemy(enemyX[e], enemyY[e], e)
    if playerX > 730:
        playerX = 730
    if playerX < 50:
        playerX = 50
    if kissY <= 38:
        kissY = 390
        kiss_state = 'ready'
    if kiss_state == "blow":
        rizzing(kissX, kissY)
        kissY -= kiss_changeY * kiss_speed**2
    if enemyY[0] >= 800:
        game_over_text()
        add_text()
    myPlayer(playerX, playerY)
    player_score()
    #game_over_text()
    pygame.display.update()
