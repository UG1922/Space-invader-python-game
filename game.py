
import pygame ,random ,math
pygame.init()
scrn = pygame.display.set_mode((800,600))
pygame.display.set_caption("my game")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#background
backIMG =  pygame.image.load('back.jpg')
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

#bullets
bulletIMG =  pygame.image.load('bullet.png')
bullet_status = "ready"
bulletY = 550
bulletX = 0

#players
playerIMG = icon
playerX = 400
playerY = 500
moveX = 0
moveY = 0

#enemy
enemyIMG = []
enemyX = []
enemyY = []
EmoveX = []
no_of_enemy = 5
for i in range(no_of_enemy):
    enemyIMG.append(pygame.image.load('enemy1.jpg'))
    enemyX.append(random.randint(50,750))
    enemyY.append(random.randint(50,300))
    EmoveX.append(1)

#score
score = 0
font = pygame.font.Font('freesansbold.ttf',32)
scoreX = 10
scoreY = 10
def score_p():
    score_D = font.render("Score :"+ str(score),True,(10,20,30))
    scrn.blit(score_D,(scoreX,scoreY))

def player(x,y):
    scrn.blit(playerIMG,(x,y))

def enemy(X,Y,i):
    scrn.blit(enemyIMG[i],(X,Y))

def bullet(x,y):
    global bullet_status
    bullet_status = "fire"
    scrn.blit(bulletIMG,(x+10,y+10))

def iscollide_player(enemyX,enemyY,playerX,playerY):
    dis_player = math.sqrt(math.pow(enemyX-playerX,2) + math.pow(enemyY-playerY,2))
    if dis_player < 50 :
        return True
    else:
        return False

def iscollide_bullet(enemyX,enemyY,bulletX,bulletY):
    dis_bullet = math.sqrt(math.pow(enemyX-bulletX,2)+ math.pow(enemyY-bulletY,2))
    if dis_bullet < 50:
        return True
    else:
        return False

def game_over_txt():
    font_1 = pygame.font.Font('freesansbold.ttf',48)
    game_over = font.render("GAME OVER",True,(10,20,30))
    scrn.blit(game_over,(350,300))
    
#driver code
running = True
while running:
    #controls
    for evnt in pygame.event.get():
        if evnt.type == pygame.QUIT:
            running = False
        if evnt.type == pygame.KEYDOWN :
            if evnt.key == pygame.K_UP:
                moveY = -1.5
            if evnt.key == pygame.K_DOWN:
                moveY = 1.5
            if evnt.key == pygame.K_LEFT:
                moveX = -1.5
            if evnt.key == pygame.K_RIGHT:
                moveX = 1.5
            if evnt.key == pygame.K_SPACE:
                if bullet_status is "ready":
                    bullet_music = pygame.mixer.Sound('laser.wav')
                    pygame.mixer.Sound.play(bullet_music)
                    pygame.mixer.Sound.set_volume(0.5)
                    bulletX = playerX
                    bulletY = playerY
                    bullet(playerX,playerY)
        if evnt.type == pygame.KEYUP:
            if evnt.key == pygame.K_LEFT or evnt.key == pygame.K_RIGHT:
                moveX = 0
            if evnt.key == pygame.K_UP or evnt.key == pygame.K_DOWN:
                moveY = 0
    #screen 
    scrn.fill((255,255,255))
    scrn.blit(backIMG,(0,0))
    #player movement
    playerX += moveX
    playerY += moveY
    if playerY >= 528:
        playerY = 528
    elif playerY < 0:
        playerY = 0
    if playerX < 0:
        playerX = 0
    elif playerX >= 758:
        playerX = 758

     #bullet movement
    if bulletY <= 0:
        bulletY = 550
        bullet_status = "ready"
    if bullet_status is "fire":
        bullet(bulletX,bulletY)
        bulletY += -2  
    
    #enemy movement
    for i in range(no_of_enemy):
        enemyX[i] += EmoveX[i]
        if enemyY[i] >= 558:
            enemyY[i] = 558
        if enemyX[i] <= 0:
            EmoveX[i] = 0.3
            enemyY[i] += 50
        elif enemyX[i] >= 758:
            EmoveX[i] = -0.3
            enemyY[i] += 50
        collide_bullet = iscollide_bullet(enemyX[i],enemyY[i],bulletX,bulletY)
        if collide_bullet:
            collision_SOUND = pygame.mixer.Sound('explosion.wav')
            pygame.mixer.Sound.play(collision_SOUND)
            pygame.mixer.Sound.set_volume(0.5)
            bulletY = 550
            bullet_status = "ready"
            score += 1
            enemyX[i] = random.randint(50,750)
            enemyY[i] = random.randint(50,300)
            
        enemy(enemyX[i],enemyY[i],i)
    
        #GAME OVER
        if iscollide_player(enemyX[i],enemyY[i],playerX,playerY) or enemyY[i] >= 500:
            game_over_txt()
            game_over_sound = pygame.mixer.Sound('game_over.wav')
            pygame.mixer.Sound.play(game_over_sound)
            pygame.mixer.Sound.set_volume(0.5)

    player(playerX,playerY)
    score_p()
    pygame.display.update()
