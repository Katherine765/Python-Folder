#ez 10x8 w/ 10m, med 18x14 w/ 40m, hard 24x20 w/ 99m
#if you click the same thing a bunch of times, it will count them as new opens

#Imports
import random as r
from tkinter import *
from copy import copy
from time import sleep, time

W = 10 ; H = 8 ; SS = 40
NUM_MINES = 10

b = {(coli,rowi): None for coli in range(W) for rowi in range(H)}
clicked = copy(b)
flagged = copy(b)

tk=Tk()
c = Canvas(tk, width=W*SS, height=H*SS+60)
c.pack()
coords={}
for coli, rowi in b.keys():
    x = coli*SS ; y = rowi*SS
    coords[(coli,rowi)] = (x,y)
    color = '#C8D8E4' if bool(coli%2==0) == bool(rowi%2==0) else '#A9BBCB'
    c.create_rectangle(x,y,x+SS,y+SS, fill=color, outline='')

def get_touching_locs(loc):
    coli = loc[0] ; rowi = loc[1]
    offsets = [-1, 0, 1]
    touching_locs = [(coli + i, rowi + j) for i in offsets for j in offsets if (coli+i, rowi+j) in b.keys()]
    touching_locs.remove((coli,rowi))
    return touching_locs

#Chooses the mine locations based on the first click, then runs the click sequence as usual
def set_up_board(e):
    click_loc = get_loc(e.x, e.y)
    placement_options = [loc for loc in b if not loc in get_touching_locs(click_loc)]
    mine_locs = r.sample(placement_options, NUM_MINES)
    for loc in mine_locs:
        b[loc] = 'm'
    for loc in b:
        touching_vals = [b[loc2] for loc2 in get_touching_locs(loc)]
        b[loc] = touching_vals.count('m')

    click(e)

def get_loc(x,y):
    return (x)//SS,(y)//SS

#Runs when a left click occurs, runs the start sequence if it is the first valid click
def click(e):
    global started
    if not started:
        if get_loc(e.x, e.y) in b:
            started = True
            set_up_board(e)
        return
    
    loc = get_loc(e.x,e.y)
    if loc in b:
        if b[loc] == 'm':
            game_over(loc)
            return
        x = coords[loc][0] + SS/2
        y = coords[loc][1] + SS/2
        if not clicked[loc]:
            clicked[loc]=c.create_text(x, y, text=b[loc], font = f'Helvetica {int(SS/2)}')
        if b[loc] == 0:
            expand(get_touching_locs(loc))

        check_for_win()
    
# flags or unflags the square
def flag(e):
    loc = get_loc(e.x,e.y)
    coord = coords[loc]
    x = coord[0] ; y = coord[1]
    if flagged[loc]:
        c.delete(flagged[loc])
        flagged[loc] = None
    else:
        flagged[loc]=c.create_rectangle(x,y,x+SS,y+SS,fill='#FF6B6B',outline='')

# continues expanding the click until there are no zeros on the outside
def expand(to_do):
    new_to_do = set()
    for loc in to_do:
        x = coords[loc][0] + SS/2
        y = coords[loc][1] + SS/2
        clicked[loc]=c.create_text(x, y, text=b[loc], font = f'Helvetica {int(SS/2)}')
        if b[loc] == 0:
            new_to_do.update(get_touching_locs(loc))
    new_to_do = {loc for loc in new_to_do if not clicked[loc]}
    if new_to_do:
        expand(new_to_do)
    

def check_for_win():
    opened = sum(1 for item in clicked.values() if item)
    if opened == W*H-NUM_MINES:
        total_time = round(time() - start_time)
        c.unbind_all('<Button-1>')
        c.unbind_all('<Button-3>')
        c.create_text((W*SS+10)/2, H*SS+35, text=f'Winner!    {total_time}s', font = 'Helvetica 20')


def game_over(bad_click_loc):
    c.unbind_all('<Button-1>') 
    c.unbind_all('<Button-3>') 
    
    mine_locs = [loc for loc in b.keys() if b[loc] == 'm']
    r.shuffle(mine_locs)
    # clicked mine will explode first
    mine_locs.remove(bad_click_loc)
    mine_locs.insert(0,bad_click_loc)
    for coli,rowi in mine_locs:
        x = coli*SS ; y=rowi*SS
        c.create_rectangle(x,y,x+SS,y+SS,fill='#80718C',outline='')
        tk.update()
        sleep(.25)

global started
started = False
start_time = time()
c.bind_all('<Button-1>', click)
c.bind_all('<Button-3>', flag)

tk.mainloop()