from copy import copy
import pygame as pg
from random import choice

W=9 ; H=9 ; SS=60 ; PAD = 7 ; FPS = 60 ; PPS = 450 # pixels per second # SS might need to be even
num_fruits = 3 ; start_length = 100 ; lengthen_amount = SS
locs = [(coli,rowi) for coli in range(W) for rowi in range(H)]
can_turn = {'Right':['Up','Down'],'Left':['Up','Down'],'Up':['Right','Left'],'Down':['Right','Left']}

class Snake:
    def __init__(s):
        s.L = start_length
        s.dots = [[0,SS/2],[s.L,SS/2]]
        s.speed = round(PPS/FPS) # pixels per frame
        s.direction = 'Right'
        s.alive = True
        s.cued_turn = None
        s.occupying_locs = [(i,0) for i in range(s.L//SS)]     

    def get_loc(s,dot):
        return dot[0]//SS, dot[1]//SS
        
    def move(s):
        
        # turn if cud and not making u-turn in same square
        if s.cued_turn and not s.get_loc(s.dots[-1]) == s.get_loc(s.dots[-2]):
            coli, rowi = s.get_loc(s.dots[-1])
            s.dots[-1] = [coli*SS+SS/2,rowi*SS+SS/2]
            coord_to_change = 0 if s.cued_turn in ('Left','Right') else 1
            sign = 1 if s.cued_turn in ('Right','Down') else -1
            new_dot = copy(s.dots[-1]) # this was the issue
            new_dot[coord_to_change] += sign * s.speed
            s.dots.append(new_dot)
            s.direction = copy(s.cued_turn)
            s.cued_turn = None
        else:
            horiz_change = s.dots[-1][0]-s.dots[-2][0] # between front two dots
            vert_change = s.dots[-1][1]-s.dots[-2][1] # between front two dots
            # this is similar code to the shortening function but differently formatted...
            if horiz_change > 0:
                s.dots[-1][0] += s.speed
            elif horiz_change < 0:
                s.dots[-1][0] -= s.speed
            elif vert_change > 0:
                s.dots[-1][1] += s.speed
            elif vert_change < 0:
                s.dots[-1][1] -= s.speed
            else:
                print('this shouldn\'t happen')

        if s.get_loc(s.dots[-1]) not in s.occupying_locs:
            s.occupying_locs.append(s.get_loc(s.dots[-1]))


    def check_life(s):
        # make sure snake is on screen
        if not s.dots[-1][0] in range(W*SS) or not s.dots[-1][1] in range(H*SS):
            snake.alive=False
            return

        # make sure the end rectangle isn't touching any other rectangles
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

            change = horiz_change if horiz_change != 0 else vert_change
            coord_to_change = 0 if horiz_change else 1
            sign = 1 if change > 0 else -1
            removing = min(extra_length, abs(change))

            s.dots[0][coord_to_change] += removing*sign
            extra_length -= removing

        try:
            s.occupying_locs = s.occupying_locs[s.occupying_locs.index(s.get_loc(s.dots[0])):]
        except:
            pass


    def display_whole_game(s, fruit_locs):
        # bg
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
            pg.draw.rect(win, "#4f7ded", pg.Rect(x,y,SS-PAD*2+2,SS-PAD*2+2))

        # fruits
        for loc in fruit_locs:
            x = loc[0]*SS+PAD
            y = loc[1]*SS+PAD
            pg.draw.rect(win, "#e7471d", pg.Rect(x,y,SS-PAD*2,SS-PAD*2))
                
        pg.display.update()

        
    def cue_turn(s,new_direction):
        if new_direction in can_turn[s.direction]:
            s.cued_turn = new_direction
            
            
    # takes two points on one line and two points on the other
    def intersection(s,P0, P1, Q0, Q1):  
        d = (P1[0]-P0[0]) * (Q1[1]-Q0[1]) + (P1[1]-P0[1]) * (Q0[0]-Q1[0]) 
        if d == 0:
            return
        t = ((Q0[0]-P0[0]) * (Q1[1]-Q0[1]) + (Q0[1]-P0[1]) * (Q0[0]-Q1[0])) / d
        u = ((Q0[0]-P0[0]) * (P1[1]-P0[1]) + (Q0[1]-P0[1]) * (P0[0]-P1[0])) / d
        if 0 <= t <= 1 and 0 <= u <= 1:
            return True
            #return round(P1[0] * t + P0[0] * (1-t)), round(P1[1] * t + P0[1] * (1-t))


class Fruits:
    def __init__(s):
        s.occupying_locs = []
    def spawn_fruit(s, snake_locs):
        empty_locs = [loc for loc in locs if not loc in snake_locs and not loc in s.occupying_locs]
        if empty_locs:
            s.occupying_locs.append(choice(empty_locs))
    def remove_fruit(s,loc):
        s.occupying_locs.remove(loc)
      
     
pg.init()
win = pg.display.set_mode((W*SS,H*SS))
clock = pg.time.Clock()
snake = Snake()
fruits = Fruits()
for _ in range(num_fruits):
    fruits.spawn_fruit(snake.occupying_locs)
score = 0
while snake.alive:
    clock.tick(FPS)
    snake.move()
    snake.shorten()
    snake.check_life()

    for loc in fruits.occupying_locs:
        if loc in snake.occupying_locs:
            score += 1
            snake.L += lengthen_amount
            fruits.remove_fruit(loc)
            fruits.spawn_fruit(snake.occupying_locs)
            break 
            
    snake.display_whole_game(fruits.occupying_locs)

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
            pg.quit()

#pg.quit()
print(f'Score: {score}')
