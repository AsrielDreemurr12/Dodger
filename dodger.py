import pygame, sys
from pygame.locals import *
from random import*
from time import*

width=600
height=600
fps=30

black=(0,0,0)
white=(255,255,255)

pygame.init()

left=False
right=False
up=False
down=False

with open('level.txt','r') as highscore_file:
    highscore=int(highscore_file.read())


slowcheat=False
reservecheat=False

score=0

a=pygame.display.set_mode((width,height))
pygame.display.set_icon(pygame.image.load('images/icon.ico'))
pygame.display.set_caption('Ловкач')
clock=pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT,3000)

duel_of_the_fates='sounds/duelofthefates.mp3'
imperial_marsh='sounds/imperialmarsh.mp3'
lst=[duel_of_the_fates,imperial_marsh]
bg_music=choice(lst)
pygame.mixer.music.load(bg_music)

pygame.mouse.set_visible(False)
mouse=False

enemy_list=pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((34,35))
        self.image.set_colorkey(black)
        self.rect=self.image.get_rect()
        self.rect.x=width//2
        self.rect.y=height-50
        self.im=pygame.image.load('images/jedi.png')
        self.image.blit(self.im,(0,0))
        a.blit(self.image,self.rect)
        self.speedx=7
        self.speedy=7

    def update(self,left,right,up,down):
        if left:
            self.rect.x-=self.speedx
            if self.rect.left < 0:
                self.speedx *= -1
        if right:
            self.rect.x+=self.speedx
            if self.rect.right > width:
                self.speedx *= -1
        if up:
            self.rect.y-=self.speedy
            if self.rect.top < 0:
                self.speedy *= -1
        if down:
            self.rect.y+=self.speedy
            if self.rect.bottom > height:
                self.speedy *= -1


    def check_for_reserve_cheat(self,reservecheat):
        if reservecheat:
            self.speedx+=2
            self.speedy+=2
        else:
            self.speedx=7
            self.speedy=7

player=Player()
food_list=pygame.sprite.Group()

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.size = randint(5, 40)
        self.image = pygame.Surface((self.size, self.size))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.im = pygame.image.load('images/sith.png')
        self.img=pygame.transform.scale(self.im,(self.size,self.size))
        self.image.blit(self.img, (0, 0))
        a.blit(self.image, self.rect)
        self.speedx = randint(-4,4)
        self.startx=self.speedx
        self.speedy = randint(2,7)
        self.starty=self.speedy

    def update(self):
        if self.rect.left < 0:
            self.speedx = -self.speedx
        if self.rect.right > width:
            self.speedx = -self.speedx
        if self.rect.top>height:
            self.kill()

        self.rect.y += self.speedy
        self.rect.x += self.speedx

    def check_for_slow_cheat(self, slowcheat):
        if slowcheat:            
            self.speedy-=2
            if self.rect.bottom<0:
                self.kill()
        else:            
            self.speedy=self.starty

class Food(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.size = randint(20, 40)
        self.image = pygame.Surface((self.size, self.size))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.im = pygame.image.load('images/cherry.png')
        self.img = pygame.transform.scale(self.im, (self.size, self.size))
        self.image.blit(self.img, (0, 0))
        a.blit(self.image, self.rect)

pygame.mixer.music.play(-1,0.0)

while True:    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            highscore_file.close()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                left=True
                right=False
            if event.key==pygame.K_RIGHT:
                right=True
                left=False
            if event.key==pygame.K_UP:
                up=True
                down=False
            if event.key==pygame.K_DOWN:
                down=True
                up=False
            if event.key==pygame.K_SPACE:
                reservecheat=True

            if event.key==pygame.K_x:
                slowcheat=True

            if event.key==pygame.K_ESCAPE:
                mouse=not mouse

        if event.type==pygame.MOUSEMOTION:
            if mouse:
                player.rect.centerx = event.pos[0]
                player.rect.centery = event.pos[1]

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT:
                left=False
                right=False
            if event.key==pygame.K_RIGHT:
                right=False
                left=False
            if event.key==pygame.K_UP:
                up=False
                down=False
            if event.key==pygame.K_DOWN:
                down=False
                up=False
            if event.key==pygame.K_SPACE:
                reservecheat=False

            if event.key==pygame.K_x:
                slowcheat=False

        if event.type==pygame.USEREVENT:
            for i in range(randint(0,7)):
                b=Enemy(randint(0,width),0)
                enemy_list.add(b)
            for j in range(randint(0,3)):
                f = Food(randint(0, width), randint(0,height))
                food_list.add(f)

    clock.tick(fps)

    a.fill(white)
    a.blit(player.image,player.rect)
    
    player.update(left,right,up,down)
    player.check_for_reserve_cheat(reservecheat)
    for i in enemy_list:
        a.blit(i.image,i.rect)
        i.update()
        i.check_for_slow_cheat(slowcheat)

    for j in food_list:
        a.blit(j.image,j.rect)

    hits=pygame.sprite.spritecollide(player,enemy_list,True)
    if hits:
        text='Игра окончена!'
        font=pygame.font.SysFont('Arial',35)
        TEXT=font.render(text,True,black)
        a.blit(TEXT,[width//2-50,height//2])
        pygame.display.update()
        sleep(4)
        if score > int(highscore):
            file=open('level.txt','w')
            file.write(str(score))
            file.close()
        pygame.quit()
        highscore_file.close()
        sys.exit()
    foods = pygame.sprite.spritecollide(player, food_list, True)
    if foods:
        score+=1

    text = 'Счёт: '+str(score)
    font = pygame.font.SysFont('Arial', 35)
    TEXT = font.render(text, True, black)
    a.blit(TEXT, [50,50])

    text = 'Рекорд: ' + str(highscore)
    font = pygame.font.SysFont('Arial', 35)
    TEXT = font.render(text, True, black)
    a.blit(TEXT, [50, 85])
    pygame.display.update()
