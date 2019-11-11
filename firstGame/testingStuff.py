import pygame
import os
pygame.init()
win= pygame.display.set_mode((500,500))

pygame.display.set_caption("First Game")



screenWidth = 500
#stands
char = pygame.image.load('standing.png')

#loads background
bg = pygame.image.load('stars.jpg')

#walks left and right
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]

score =0

bulletSound = pygame.mixer.Sound('gun_shot.wav')
enemyHit = pygame.mixer.Sound('enemyHit.wav')
manHit = pygame.mixer.Sound('playerGrunt.wav')
music = pygame.mixer.music.load('musicForGame.mp3')

pygame.mixer.music.play(-1)
#Enemy
class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y =y
        self.width =width
        self.height = height
        self.end = end
        self.walkCount =0
        self.vel = 3
        self.path= [self.x,self.end]
        self.hitbox =(self.x+17,self.y+2,31,57)
        self.health = 10
        self.visible = True
    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount + 1>= 33:
                self.walkCount =0
            if self.vel >0:
                win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            else:
                win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            pygame.draw.rect(win,(255,0,0),(self.hitbox[0],self.hitbox[1]-20,50,10))
            pygame.draw.rect(win,(0,255,0),(self.hitbox[0],self.hitbox[1]-20,50-(5*(10-self.health)),10))
            self.hitbox =(self.x+17,self.y+2,31,57)
      #  pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def move(self):
        
        if(self.vel>0):
            if self.x+self.vel<self.path[1]:
                self.x+=self.vel
            else:
                self.vel = self.vel*-1
                self.walkCount = 0
        else:
            if self.x -self.vel >self.path[0]:
                self.x +=self.vel
            else:
                self.vel = self.vel*-1
                self.walkCount = 0
       
    def hit(self):
        if self.health>1:
            self.health -=1
        else:   
            self.visible = False
            
#Projectile class
class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8*facing


    def draw(self,win):
        pygame.draw.circle(win,self.color, (self.x,self.y),self.radius)



#player class
class player(object):
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.height = height
        self.width = width
        self.vel = 5
        self.isJump =False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing =True
        self.hitbox= (self.x+17,self.y+11,29,52)
    def draw(self,win):
        #checks to ensure that you aren't using to many frames
        if self.walkCount +1 >=27:
            self.walkCount =0

        if not self.standing :
            if self.left:
                #walks left
                win.blit(walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            elif self.right:
            #walks right
                win.blit(walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
        else:
            if  self.right:
                win.blit(walkRight[0],(self.x,self.y))
            else:
                win.blit(walkLeft[0],(self.x,self.y))
        self.hitbox= (self.x+17,self.y+11,29,52)
       # pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def hit(self):
        self.isJump =False
        self.jumpCount=10
        self.x=60
        self.y = 410
        self.walkCount =0
        font1 = pygame.font.SysFont('comicsans',100)
        text = font1.render('-5',1,(255,0,0))
        win.blit(text,(500/2-(text.get_width()/2),(500/2-(text.get_height()))))
        pygame.display.update()
        i = 0
        while (i<100):
            pygame.time.delay(10)
            i+=1
            for event in pygame.event.get():
                if event.type ==pygame.QUIT:
                    i=301
                    pygame.quit()
            
        


def redrawGameWindow():
    win.blit(bg,(0,0))
    man.draw(win)
    goblin.draw(win)
    text = font.render('Score: ' +str(score),1,(255,255,255))
    win.blit(text,(300,10))
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()




#creates clock
clock = pygame.time.Clock()

#Createsfont that is boled and not italics that is Times New Roman
font = pygame.font.SysFont('Times New Roman',30,True,False)



#creates instance of player

man = player(300,410,64,64)

man.left = True
#creates instance of Enemy

goblin = enemy(100,410,64,64,450)
#number of shots
shootLoop=0

#creates instance of bullet
bullets = []

#loop that runs game
run = True
while run:
    #frame rate
    clock.tick(27)
    if goblin.visible==True:
        if man.hitbox[1]<goblin.hitbox[1]+goblin.hitbox[3] and man.hitbox[1]+man.hitbox[3] >goblin.hitbox[1]:
            if man.hitbox[0]+ man.hitbox[2]>goblin.hitbox[0]and man.hitbox[0]<goblin.hitbox[0]+goblin.hitbox[2]:
                manHit.play()
                man.hit()
                if score -5 >0:
                    score -= 5
                else:
                    score =0
           
    if shootLoop>0:
        shootLoop+=1
    if shootLoop>3:
        shootLoop=0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

    for bullet in bullets:
        if bullet.y -bullet.radius <goblin.hitbox[1]+goblin.hitbox[3] and bullet.y+bullet.radius >goblin.hitbox[1]:
            if bullet.x+ bullet.radius>goblin.hitbox[0]and bullet.x-bullet.radius<goblin.hitbox[0]+goblin.hitbox[2]:
                enemyHit.play()
                goblin.hit()
                score = score+1
                bullets.pop(bullets.index(bullet))



        if bullet.x <500 and bullet.x > 0:
            bullet.x+=bullet.vel
        else:
            bullets.pop(bullets.index(bullet))



    #gets keys pressed
    keys =pygame.key.get_pressed()

    #fires bullets
    if keys[pygame.K_SPACE] and shootLoop==0:
        bulletSound.play()
        if man.left:
            facing =-1
        else:
            facing = 1
        if len(bullets)<5:
            bullets.append(projectile(round(man.x+man.width//2),round(man.y+man.height//2),6,(0,0,0),facing ))
        shootLoop =1

    if keys[pygame.K_LEFT] and man.x>0:
        #moves left
        man.x-=man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT]and man.x<screenWidth-man.width:
        #moves right
        man.x+=man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        walkCount = 0

    if not(man.isJump):
        #checks if you've pressed the "jump" button
        if keys[pygame.K_UP]:
            man.isJump =True
            man.walkCOunt = 0
    else:
        if man.jumpCount>=-10:
            neg =1
            if man.jumpCount<0:
                neg = -1
                #jumps
            man.y-=(man.jumpCount ** 2)/2*neg
            man.jumpCount-=1
        else:
            man.isJump=False
            man.jumpCount=10
    redrawGameWindow()


pygame.quit()
