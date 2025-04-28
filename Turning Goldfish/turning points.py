from shape import draw_triangle
from time import sleep
from copy import copy
from tkinter import *
import math

# either have them both called right or both called player one


WIDTH = 4 ; HEIGHT = 3
SQUARE_SIZE = 100 ; FISH_SIZE = SQUARE_SIZE * .75
directions = {'up':(0,-1),'right':(1,0),'down':(0,1),'left':(-1,0)}

# will store orientation of that square in future
grid = {(x,y): None for x in range(WIDTH) for y in range(HEIGHT)}


# Set up board
tk = Tk()
canvas = Canvas(tk, width=WIDTH*SQUARE_SIZE+10, height=HEIGHT*SQUARE_SIZE+60)
canvas.pack()
coords = {}
for loc in grid.keys():
    startx = loc[0]*SQUARE_SIZE + 5
    starty = loc[1]*SQUARE_SIZE + 5
    coords[loc] = (startx+SQUARE_SIZE/2,starty+SQUARE_SIZE/2)
    canvas.create_rectangle(startx,starty,startx+SQUARE_SIZE,starty+SQUARE_SIZE, fill='white', outline='black')


#canvas stuff
images = copy(grid)
turn = 'right'
text = canvas.create_text((WIDTH*SQUARE_SIZE+10)/2, HEIGHT*SQUARE_SIZE+35, text=f'{turn}\'s turn', font = 'Helvetica 20')


# given canvas coordinates, returns a locations that can be used within the dictionaries
def get_square_loc(x,y):
    return (x-5)//SQUARE_SIZE,(y-5)//SQUARE_SIZE

# returns the blocks touching in cardinal directions
def get_touching_locs(loc):
    x = loc[0] ; y = loc[1]
    touching_locs = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    return [loc for loc in touching_locs if loc in grid.keys()]

def get_direction(event, loc):
    dx = event.x-coords[loc][0] 
    dy = event.y-coords[loc][1]
    if abs(dx)>abs(dy):
        if dx > 0:
            return 'right'
        if dx < 0:
            return 'left'
    if abs(dx)<abs(dy):
        if dy > 0:
            return 'down'
        if dy < 0:
            return 'up'


def click(event):
    loc = get_square_loc(event.x,event.y)
    
    if not loc in grid or grid[loc]:
        return

    direction = get_direction(event, loc)
    print(direction)
    
    if not direction:
        return
    
    grid[loc] = direction
    images[loc]=draw_triangle(canvas, coords[loc][0], coords[loc][1], FISH_SIZE, direction)

    tx = loc[0]+directions[direction][0]
    ty = loc[1]+directions[direction][1]

    global turn
    global text
    turn = 'right' if turn=='left' else 'left'
    canvas.delete(text)
    text = canvas.create_text((WIDTH*SQUARE_SIZE+10)/2, HEIGHT*SQUARE_SIZE+35, text=f'{turn}\'s turn', font = 'Helvetica 20')
    
    recursion(tx,ty)


    
    if not None in grid.values():
        end_of_game()


def recursion(tx,ty):
    target = (tx,ty)
    if target in grid and grid[target]:
        direction = grid[target]
        
        keys = list(directions.keys())
        new_direction = keys[keys.index(direction)+1-4]

        grid[target] =  new_direction
        canvas.delete(images[target])
        images[target] = draw_triangle(canvas, coords[target][0], coords[target][1], FISH_SIZE, new_direction)

        # redefining for the next target
        tx += directions[new_direction][0]
        ty += directions[new_direction][1]

        tk.update()
        sleep(.2)
        
        recursion(tx,ty)


def end_of_game():
    global text
    canvas.delete(text)
    
    left  = 0
    right = 0
    for loc in grid:
        if grid[loc] == 'right':
            right +=1
        elif grid[loc] == 'left':
            left += 1

    if right > left:
        canvas.create_text((WIDTH*SQUARE_SIZE+10)/2, HEIGHT*SQUARE_SIZE+35, text=f'Right wins!', font = 'Helvetica 20')
    elif left < right:
        canvas.create_text((WIDTH*SQUARE_SIZE+10)/2, HEIGHT*SQUARE_SIZE+35, text=f'Left wins!', font = 'Helvetica 20')
    else:
        canvas.create_text((WIDTH*SQUARE_SIZE+10)/2, HEIGHT*SQUARE_SIZE+35, text=f'Tie.', font = 'Helvetica 20')

canvas.bind_all('<Button-1>', click)
