import pygame, random, time

from pygame.locals import *
from pygame import mixer 


class Enemy(pygame.sprite.Sprite):
    def __init__ (self, x, y):
        super().__init__()
        self.imageList = ["alien.png", "alien2.png"]
        self.currentImagePosition = 0
        self.currentImage = pygame.image.load(self.imageList[self.currentImagePosition])
        self.surf = pygame.Surface((40,40))
        self.x = x
        self.y = y
        self.rect = self.surf.get_rect(center = (self.x,self.y))
        self.direction = "left"
        self.imageReset = 0
        
    def move (self, destroyed, playerScore, speed):
        if self.direction == "left":
            self.rect.move_ip(-speed,0)
            
        if self.direction == "right":
            self.rect.move_ip(speed,0)

    def left(self):
        self.rect.top += 32
        self.direction = "left"

    def right(self):
        self.rect.top += 32
        self.direction = "right"

    def reset(self):
        self.rect = self.surf.get_rect(center = (self.x,self.y))


    def draw(self, window):
        
        if self.imageReset == 60 and self.currentImagePosition == 1:
            self.currentImagePosition = 0
            self.imageReset = 0
                
        if self.imageReset == 60 and self.currentImagePosition == 0:
            self.currentImagePosition = 1
            self.imageReset = 0
            
        self.imageReset+=1    
        self.currentImage = pygame.image.load(self.imageList[self.currentImagePosition])
        window.blit(self.currentImage, self.rect)
        
        
class enemySpawner(pygame.sprite.Sprite):
    alienList = []
    def __init__(self):
        self.edgeBuffer = 50
        self.alienBuffer = 20
        self.alienWidth = 32
        
        for x in range(self.edgeBuffer, 500, self.alienWidth+self.alienBuffer):
            for y in range(self.edgeBuffer, 300, self.alienWidth+32):
                self.alienList.append(Enemy(x,y))


class Player(pygame.sprite.Sprite):
    def __init__ (self, screenWidth, screenHeight):
        super().__init__()
        self.image = pygame.image.load("player.png")
        self.surf = pygame.Surface((32,32))
        self.rect = self.surf.get_rect(midbottom = (screenWidth / 2.0, screenHeight))


    def move(self, screenWidth, screenHeight):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5,0)

        if self.rect.right < screenWidth:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5,0)

    def draw(self,window):
        window.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__ (self, player):
        super().__init__()
        self.image = pygame.image.load("bullet.png")
        self.surf = pygame.Surface((10, 10))
        self.rect = self.surf.get_rect(center = (player.rect.midtop))
        self.fired = False
           
    def move(self):
        self.rect.move_ip(0,-5)

    def draw(self, window):
        window.blit(self.image, self.rect)


class Background():
    def __init__ (self,DISPLAYSURFACE):
        self.backgroundImage = pygame.image.load("clouds.png")
        self.rectBGimage = self.backgroundImage.get_rect()
        self.moveSpeed = 0.5
        self.bgX1 = 0
        self.bgY1 = 0
        self.bgX2 = -(self.rectBGimage.width+self.moveSpeed)
        self.bgY2 = 0

    def update(self):
        self.bgX1 += self.moveSpeed
        self.bgX2 += self.moveSpeed
        if self.bgX1 >= self.rectBGimage.width:
            self.bgX1 = -(self.rectBGimage.width+self.moveSpeed)

        if self.bgX2 >= self.rectBGimage.width:
            self.bgX2 = -(self.rectBGimage.width+self.moveSpeed)

    def render(self,DISPLAYSURFACE):
        DISPLAYSURFACE.blit(self.backgroundImage,(self.bgX1, self.bgY1))
        DISPLAYSURFACE.blit(self.backgroundImage,(self.bgX2, self.bgY2))


def main():
    pygame.init()
    FPS = 60
    clock = pygame.time.Clock()
    speed = 1
    score = 0
    wait = 0
    imageReset = 0

    #Colours
    black = (0,0,0)
    red = (255,0,0)
    green = (0, 255, 0)
    colourIncVal = 0
    white = (255,255,255)

    #Fonts
    font = pygame.font.SysFont("Verdana", 60)
    smallFont = pygame.font.SysFont("Verdana", 20)
    gameOverFont = smallFont.render("Game Over", True, black)

    #Create Game Window
    screenWidth = 500
    screenHeight = 600

    backgroundImage = pygame.image.load("backgroundImage.png")
    DISPLAYSURFACE = pygame.display.set_mode((screenWidth,screenHeight))
    pygame.display.set_caption("Space Invaders!")

    INCREASE_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INCREASE_SPEED, 3000)

    # Playing Music
    mixer.init() 
    mixer.music.load("8bit.mp3") 
    mixer.music.set_volume(0.7) 
    mixer.music.play()

    #Initialise the background, player, bullet and enemies
    background = Background(DISPLAYSURFACE)
    player = Player(screenWidth, screenHeight)
    bulletList = []
    enemySpawner()
    enemyGroup = pygame.sprite.Group()
    
    for x in enemySpawner.alienList:
        enemyGroup.add(x)

    while True:
                
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                
            if event.type == INCREASE_SPEED:
                speed += 0.1
        
        if colourIncVal > 254:
            DISPLAYSURFACE.fill((0,0,255))

        else:
            DISPLAYSURFACE.fill((0,0,0+colourIncVal))
            colourIncVal += 0.2
        
        background.update()
        background.render(DISPLAYSURFACE)
        player.draw(DISPLAYSURFACE)
        player.move(screenWidth,screenHeight)
        scoreText = smallFont.render("Score: "+str(score), True, white)
        DISPLAYSURFACE.blit(scoreText, (0,0))

        if len(enemyGroup) == 0:
            enemySpawner.alienList = []
            enemySpawner()
            enemyGroup = pygame.sprite.Group()
            for x in enemySpawner.alienList:
                enemyGroup.add(x)
        
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys [K_SPACE] and wait > 30:
            bulletList.append(Bullet(player))
            wait = 0
            
        for x in bulletList:
            if x.rect.top < 2:
                bulletList.remove(x)
            x.move()
            x.draw(DISPLAYSURFACE)

        for enemy in enemyGroup:
            
            enemy.move(False, 0, speed)
            enemy.draw(DISPLAYSURFACE)

            if enemy.rect.left < 0:
                enemy.right()
            if enemy.rect.right > 500:
                enemy.left()
            if enemy.rect.bottom > 600:
               DISPLAYSURFACE.fill(red)
               DISPLAYSURFACE.blit(gameOverFont, (200,250))
               DISPLAYSURFACE.blit(scoreText, (215,300))
               pygame.display.update()
               time.sleep(4)
               enemySpawner.alienList = []
               enemySpawner()
               enemyGroup = pygame.sprite.Group()
               
               for x in enemySpawner.alienList:
                   enemyGroup.add(x)
               for resetEnemy in enemyGroup:
                   resetEnemy.reset()
               score = 0
               speed = 1


                
            for bullet in bulletList:
                if pygame.sprite.spritecollide(enemy, bulletList, False):
                    enemy.kill()
                    bulletList.remove(bullet)
                    score = score + 10
                    
        pygame.display.update()
        imageReset +=1
        wait += 1
        clock.tick(FPS)

main()
