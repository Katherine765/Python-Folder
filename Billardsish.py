import pygame as pg
import math

R = 20 ; W = 1000 ; H = 500
FRIC = 70 # pixels / sec
ballColors = [
    (255, 85, 85),     # Bright Red
    (255, 153, 51),    # Tangerine Orange
    (255, 221, 51),    # Sunny Yellow
    (153, 255, 51),    # Lime Green
    (51, 204, 204),    # Bright Aqua
    (102, 153, 255),   # Sky Blue
    (204, 102, 255),   # Soft Violet
    (255, 102, 178),   # Rose Pink
    (255, 204, 153),   # Apricot
    (204, 255, 153),   # Spring Green
    (153, 255, 204),   # Mint
    (153, 204, 255),   # Periwinkle
    (255, 153, 204),   # Cotton Candy
    (255, 255, 153),   # Light Yellow
    (200, 200, 200)    # Light Gray
]

def getBallStartPoss():
    biggerR = R + 1
    positions = []
    start_x = W- W // 4
    start_y = H // 2
    for col in range(5):
        num_balls = col + 1
        offset_y = col * biggerR
        for i in range(num_balls):
            x = start_x + (col * math.sqrt(3) * biggerR)
            y = start_y - offset_y + (i * 2 * biggerR)
            positions.append((x, y))
    return positions


class Ball:
    def __init__(s, x, y, color = 'white'):
        s.x = x ; s.y = y  # pixels
        s.xv = 0 ; s.yv = 0  # pixels / sec
        s.color = color

    def move(s, dt):
        s.x += s.xv * dt
        s.y += s.yv * dt
        theta = math.atan2(s.y, s.x)

        def applyFriction(v):
            if abs(v) < 5:
                return 0 # stop jittering
            return max(0, abs(v - FRIC*math.cos(theta)*dt)) if v > 0 else min(0, v + FRIC*math.sin(theta)*dt)
        s.xv = applyFriction(s.xv)
        s.yv = applyFriction(s.yv)


    def isTouching(s, ball):
        dx = s.x - ball.x
        dy = s.y - ball.y
        return dx*dx + dy*dy < (2*R)**2 + 1

    def draw(s, win):
        pg.draw.circle(win, s.color, (s.x, s.y), R)


class cueBall(Ball):
    def __init__(s, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def push(s, mouseX, mouseY):
        theta = math.atan2(mouseY-s.y, mouseX-s.x)
        pushSpeed = min(.4*W, math.sqrt((mouseX-s.x)**2+(mouseY-s.y)**2)) * 1100/(.4*W)
        s.xv = pushSpeed * math.cos(theta)
        s.yv = pushSpeed * math.sin(theta)


class Game:
    def __init__(s):
        s.cueBall = cueBall(50, H/2)
        startPoss = getBallStartPoss()
        s.balls = [Ball(*startPoss[i], color=ballColors[i]) for i in range(15)] + [s.cueBall]

    def run(s):
        pg.init()
        win = pg.display.set_mode((W, H))
        clock = pg.time.Clock()

        def rotateVels(xv, yv, theta):
            return xv*math.cos(theta) - yv*math.sin(theta), xv*math.sin(theta) + yv*math.cos(theta),

        while s.balls:
            dt = clock.tick(120) / 1000
            win.fill("black")

            for b in s.balls:
                b.move(dt)

            for i, b1 in enumerate(s.balls[:-1]):
                for b2 in s.balls[i+1:]:
                    dx = b2.x - b1.x
                    dy = b2.y - b1.y
                    distSquared = dx*dx + dy*dy
                    if distSquared < (2*R)**2:
                        theta = math.atan2(dy, dx)
                        parrv1, perpv1 = rotateVels(b1.xv, b1.yv, theta)
                        parrv2, perpv2 = rotateVels(b2.xv, b2.yv, theta)
                        parrv1, parrv2 = parrv2, parrv1
                        b1.xv, b1.yv = rotateVels(parrv1, perpv1, -theta)
                        b2.xv, b2.yv = rotateVels(parrv2, perpv2, -theta)

                        # stop overlapping
                        sep = (2*R - math.sqrt(distSquared)) / 2
                        b1.x -= math.cos(theta) * sep
                        b1.y -= math.sin(theta) * sep
                        b2.x += math.cos(theta) * sep
                        b2.y += math.sin(theta) * sep
                # wall
                for b in s.balls:
                    if b.x <= R:
                        b.x=R ; b.xv*=-1
                    elif b.x >= W-R:
                        b.x=W-R ; b.xv*=-1
                    if b.y <= R:
                        b.y=R ; b.yv*=-1
                    elif b.y >= H-R:
                        b.y=H-R ; b.yv*=-1

            for b in s.balls:
                b.draw(win)
            pg.display.flip()

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    return
                if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                    s.cueBall.push(*e.pos)
            
Game().run()