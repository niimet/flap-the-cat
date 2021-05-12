# flap-the-cat
My first game that i published
!! Note i didnt create this game. It's not my own project but i watched some tutorials and adapted with my own skills.


import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_w = 864
screen_h = 936

screen = pygame.display.set_mode((screen_w,screen_h))
pygame.display.set_caption('Flappy Bird')

#define font
font = pygame.font.SysFont('Bauhaus',60)

#define color
white = (255,255,255)

#define game variable

ground_scroll = 0
scroll_speed = 4
flying = False
gameover = False
pipe_gap = 150
pipe_frequency = 1500#miliseconds
last_pipe = pygame.time.get_ticks()
score = 0
pass_pipe = False


#loag images

bg = pygame.image.load('resimler/bg.png')
gr = pygame.image.load('resimler/ground.png')
button_img = pygame.image.load('resimler/restart.png')

def draw_text(text,font,textc,x,y):
    img = font.render(text,True,textc)
    screen.blit(img,(x,y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_h/2)
    score = 0
    return score

#sprite class has already draw and update functions that built into them
class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #image her zaman kullanılmalıdır sprite clasında ve rect ve pozsiyson
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f'resimler/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False

    def update(self):
        #gravity
        if flying:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom  < 768 :
                self.rect.y += int(self.vel)

            if not gameover:
                #jump
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    self.vel = -10
                if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                    self.clicked = False

                #handle the animation
                self.index += 1
                self.index = self.index % len(self.images)
                self.image = self.images[self.index]

                #rotate the bird
                #1 we need to source in the one we want to rotate
                self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
            else:
                self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resimler/pipe.png')
        self.rect = self.image.get_rect()
        self.pipespeed = 0
        #position 1 is from the top, and -1 from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image,False, True)
            self.rect.bottomleft = [x,y - int(pipe_gap/2)]

        if position == -1:
            self.rect.topleft = [x,y + int(pipe_gap/2)]

    def update(self):
        if not gameover:
            self.rect.x -= scroll_speed
        if self.rect.right < 0 :
            self.kill()

class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):
        action = False
        #get mouse pos
        pos = pygame.mouse.get_pos()
        #check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        #draw button
        screen.blit(self.image,(self.rect.x,self.rect.y))
        return action




#group'ta sprite fonksiyonları ile birlikte gelmekte, bird group keeps a track of all of the sprites !!, almost like python list in a way after doing that add this to drawing part
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_h / 2))
#since it is acting like a python list its like appending an item to a list but we are using add instead of append !
bird_group.add(flappy)
#class oluşturduktan sonra group kısmına ekle!!
button_group = pygame.sprite.Group()
button = Button(screen_w/2,screen_h/2,button_img)


run = True

while run:

    clock.tick(fps)

    #Arka plana resim koymak için
    screen.blit(bg,(0,0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    pipe_group.update()
    # draw ground
    screen.blit(gr, (ground_scroll, 768))

    #check the score
    if len(pipe_group) > 0 :
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
                and not pass_pipe:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                print(score)
                pass_pipe = False

    draw_text(str(score),font,white,int(screen_w/2),20)



    #look for collision, first group bird second pipe, reason to false is to delete the sprite
    if pygame.sprite.groupcollide(bird_group,pipe_group,False,False) or flappy.rect.top < 0:
        gameover = True




    #check if bird has hit the ground
    if flappy.rect.bottom > 768:
        gameover = True
        flying = True

    if gameover:
        if button.draw():
            print('clicked')
            gameover = False
            score = reset_game()

    #ground çiz
    if not gameover and flying == True:

        #generate new pipe
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100,100)
            btm_pipe = Pipe(screen_w, int(screen_h / 2) + pipe_height, -1)
            top_pipe2 = Pipe(screen_w, int(screen_h / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe2)
            last_pipe = time_now


        ground_scroll -= scroll_speed

        if abs(ground_scroll) > 35:
            ground_scroll = 0


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and  flying == False and gameover == False:
             flying = True

    #yukarıda olan herşeyi günceller
    pygame.display.update()

pygame.quit()
