import math
import pygame as pg
import random as r

# to-do: get rid of bounce bounce oddities, make paddle not go out of bounds

W = 1000 ; H = 600

pg.init()
win = pg.display.set_mode((W,H))
font = pg.font.SysFont('arialblack',50)
clock = pg.time.Clock()

class Paddle:
    def __init__(s, width):
        s.topy = H-40
        s.width = width
        s.rect = pg.Rect(pg.mouse.get_pos()[0]-s.width/2,s.topy, s.width, 20)
        s.score = 0
    
    def update(s):
        s.rect = pg.Rect(pg.mouse.get_pos()[0]-s.width/2,s.topy, s.width, 20)
        pg.draw.rect(win, 'green', s.rect)
    
class Ball:
    def __init__(s, radius, speed):
        s.x = W/2
        s.y = radius
        s.radius = radius
        s.speed = speed
        s.angle = r.randint(45,135)
        
    def update(s):
        s.x += s.speed * math.cos(math.radians(s.angle))
        s.y += s.speed * math.sin(math.radians(s.angle))
        pg.draw.circle(win, 'green', (s.x,s.y), s.radius)

        if s.x <= s.radius or s.x >= W - s.radius:
            s.angle = 180 - s.angle
        elif s.y <= s.radius:
            s.angle *= -1

def manageX():
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            quit()


paddle = Paddle(150)
ball = Ball(30, 15)
score = 0
while ball.y+ball.radius <= H:
    win.fill('black')
    paddle.update()
    ball.update()
    win.blit(font.render(str(score), False, 'white'), (10,0))
    pg.display.update()

    if paddle.topy <= ball.y+ball.radius and pg.mouse.get_pos()[0] - paddle.width/2 <= ball.x <= pg.mouse.get_pos()[0] + paddle.width/2:
        ball.angle = r.randint(180+20, 360-20) # the 20s make the bounces not as extreme
        ball.speed += 1
        score += 1

    manageX()
    clock.tick(30)

while True:
    manageX()