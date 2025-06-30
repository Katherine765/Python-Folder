import pygame as pg
import random as r
import time

W = 1000 ; H = 600

pg.init()
win = pg.display.set_mode((W,H))
font = pg.font.SysFont('arialblack',50)
clock = pg.time.Clock()

class Bird:
    def __init__(s, x, g, jumpVel, size):
        s.x = x
        s.g = g
        s.jumpVel = jumpVel
        s.size = size

        s.pos = H/2
        s.vel = 0
        s.rect = pg.Rect(s.x,s.pos, s.size, s.size)
    
    def update(s):
        s.pos += s.vel
        s.vel += s.g
        s.rect = pg.Rect(s.x, s.pos, s.size, s.size)
        pg.draw.rect(win, 'yellow', s.rect)

    def jump(s):
        s.vel = s.jumpVel
    

class Pipe:
    def __init__(s, vel, size, gapSize):
        s.vel = vel
        s.size = size
        s.gapSize = gapSize

        s.pos = W
        s.gapPos = r.randint(0, H-s.gapSize)
        s.rect1 = pg.Rect(s.pos, 0, s.size, s.gapPos)
        s.rect2 = pg.Rect(s.pos, s.gapPos+s.gapSize, s.size, H-s.gapPos-s.gapSize)

        s.onScreen = True
        s.pastBird = False
        
    def update(s):
        s.pos += pipe.vel
        if s.pos < -pipe.size:
            s.onScreen = False
        
        s.rect1 = pg.Rect(s.pos, 0, pipe.size, s.gapPos)
        s.rect2 = pg.Rect(s.pos, s.gapPos+pipe.gapSize, pipe.size, H-s.gapPos-pipe.gapSize)
        pg.draw.rect(win, 'green', s.rect1)
        pg.draw.rect(win, 'green', s.rect2)

# end of classes

def checkLiveness():
    for pipe in pipes:
        if bird.rect.colliderect(pipe.rect1) or \
           bird.rect.colliderect(pipe.rect2) or \
           not 0 < bird.pos < H-bird.size:
            return False 
    return True

def manageX():
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            quit()


bird = Bird(75, 2.5, -18, 35)
pipes = []
score = 0
pipeTimeIncrement = 1.25
lastPipeTime = -999

while checkLiveness():
    win.fill('black')
    bird.update()
    for pipe in pipes:
        pipe.update()
        if pipe.pos + pipe.size < 75 and not pipe.pastBird:
            score += 1
            pipe.pastBird = True
    win.blit(font.render(str(score), False, 'white'), (10,0))
    pg.display.update()

    # remove old and add new pipes
    pipes = [pipe for pipe in pipes if pipe.onScreen]
    if time.time()-lastPipeTime >= pipeTimeIncrement:
        pipes.append(Pipe(-8, 75, 220))
        lastPipeTime = time.time()

    if pg.key.get_pressed()[pg.K_UP]:
        bird.jump() 
    manageX()
    clock.tick(30)

while True:
    manageX()