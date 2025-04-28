from copy import copy
import pygame as pg
import time

# can always draw rectangles at joints so it doesn't look funky, idk if i'd have to think abt directions to do that

# need to keep track of which snap locations the snake touches
# the fruit can go to any snap loc that doesn't have snake in it
# and fruit is eaten when it is in a snake loc

# would drawing bg as one big rectangle w/ only half of the checkered squares (the ones of the other color) on top be better?

W=10 ; H=10 ; SS=50 ; PAD = 10 ; FPS = 60 ; pixels_per_second = 100
snap_locations = [(coli*SS+SS/2,rowi*SS+SS/2) for coli in range(W) for rowi in range(H)]
can_turn = {'Right':['Up','Down'],'Left':['Up','Down'],'Up':['Right','Left'],'Down':['Right','Left']}
            

class Snake:
    def __init__(s):
        s.L = 300 # length
        s.dots = [[0,int(SS/2)],[s.L,int(SS/2)]]
        s.speed = round(pixels_per_second/FPS)
        s.direction = 'Right'
        s.alive = True
        s.cued_turn = None
        
    def move(s):
        pixels_to_move = s.speed
        while pixels_to_move:
            # turn if necessary
            if s.cued_turn and tuple(s.dots[-1]) in snap_locations:
                coord_to_change = 0 if s.cued_turn in ('Left','Right') else 1
                sign = 1 if s.cued_turn in ('Right','Down') else -1
                new_dot = copy(s.dots[-1])
                new_dot[coord_to_change] += sign
                s.dots.append(new_dot)
                s.direction = copy(s.cued_turn)
                s.cued_turn = None
                pixels_to_move -= 1
                continue

            horiz_change = s.dots[-1][0]-s.dots[-2][0] # between front two dots
            vert_change = s.dots[-1][1]-s.dots[-2][1] # between front two dots
            # this is similar code to the shortening function but differently formatted...
            if horiz_change > 0:
                s.dots[-1][0] += 1
            elif horiz_change < 0:
                s.dots[-1][0] -= 1
            elif vert_change > 0:
                s.dots[-1][1] += 1
            elif vert_change < 0:
                s.dots[-1][1] -= 1
            else:
                print('this shouldn\'t happen')
            pixels_to_move -= 1


        # make sure snake is on screen
        if not s.dots[-1][0] in range(W*SS) or not s.dots[-1][1] in range(H*SS):
            snake.alive=False

        # make sure the end rectangle isn't touching any other rectangles (other intersections should already have been discovered earlier, unless several new lines were just formed
        endline_p1 = s.dots[-2]
        endline_p2 = s.dots[-1]
        prev_p = s.dots[0]
        for p in s.dots[1:-2]: # -2 bc we don't want to compare to the second most-recent line, obviously its touching that 
            if s.intersection(prev_p,p,endline_p1,endline_p2):
                snake.alive = False
                return
            prev_p = copy(p)


    def shorten(s):
        prev_dot = s.dots[0]
        actual_length = 0
        for dot in s.dots[1:]:
            actual_length += abs(dot[0]-prev_dot[0]) + abs(dot[1]-prev_dot[1]) # one addend will be 0
            prev_dot = copy(dot)
        extra_length = actual_length - s.L

        while extra_length:
            if s.dots[0] == s.dots[1]:
                del s.dots[0]
            
            horiz_change = s.dots[1][0]-s.dots[0][0] # between back two dots
            vert_change = s.dots[1][1]-s.dots[0][1] # between back two dots
            if horiz_change:
                coord_to_change = 0
                sign = 1 if horiz_change>0 else -1
                max_change = abs(horiz_change)
            elif vert_change:
                coord_to_change = 1
                sign = 1 if vert_change>0 else -1
                max_change = abs(vert_change)
            else:
                print('this shouldn\'t happen 2')  

            removing = min(extra_length, max_change)
            s.dots[0][coord_to_change] += removing*sign
            extra_length -= removing


    def display(s):
        # background
        for coli in range(W):
            for rowi in range(H):
                x = coli*SS ; y = rowi*SS
                color = '#aad751' if bool(coli%2 == 0) == bool(rowi%2 == 0) else '#a2d149'
                pg.draw.rect(win,color,pg.Rect(x,y,SS,SS))

        # snake lines
        prev_dot = s.dots[0]
        for dot in s.dots[1:]:
            pg.draw.line(win, "#4f7ded", prev_dot, dot, SS-PAD*2)
            prev_dot = copy(dot)

        # snake joints
        for dot in s.dots[1:-1]:
            x = dot[0] - SS/2 + PAD
            y = dot[1] - SS/2 + PAD
            pg.draw.rect(win, "#4f7ded", pg.Rect(x,y,SS-PAD*2,SS-PAD*2))

        pg.display.update()

        
    def cue_turn(s,new_direction):
        if new_direction in can_turn[s.direction]:
            s.cued_turn = new_direction


    # takes two points on one line and two points on the other
    # function coppied from stack overflow
    def intersection(s,P0, P1, Q0, Q1):  
        d = (P1[0]-P0[0]) * (Q1[1]-Q0[1]) + (P1[1]-P0[1]) * (Q0[0]-Q1[0]) 
        if d == 0:
            return None
        t = ((Q0[0]-P0[0]) * (Q1[1]-Q0[1]) + (Q0[1]-P0[1]) * (Q0[0]-Q1[0])) / d
        u = ((Q0[0]-P0[0]) * (P1[1]-P0[1]) + (Q0[1]-P0[1]) * (P0[0]-P1[0])) / d
        if 0 <= t <= 1 and 0 <= u <= 1:
            return round(P1[0] * t + P0[0] * (1-t)), round(P1[1] * t + P0[1] * (1-t))
        return None



class Fruit:
    def __init__(s):
        s.positions = []
    def spawn(s):
        pass
     
pg.init()
win = pg.display.set_mode((W*SS,H*SS))
clock = pg.time.Clock()
snake = Snake()
while snake.alive:
    clock.tick(FPS)
    snake.move()
    snake.shorten()
    snake.display()

    keys = pg.key.get_pressed()
    if keys[pg.K_RIGHT]:
        snake.cue_turn('Right')
    elif keys[pg.K_LEFT]:
        snake.cue_turn('Left')
    elif keys[pg.K_UP]:
        snake.cue_turn('Up')
    elif keys[pg.K_DOWN]:
        snake.cue_turn('Down')
        
    
    for e in pg.event.get():
        if e.type == pg.QUIT:
            snake.alive = False
            break

pg.quit()
