#ez 10x8 w/ 10m, med 18x14 w/ 40m, hard 24x20 w/ 99m
# b stores 'm' for mines and # mines touching otherwise, bad naming but im not fixing that

import random as r
from tkinter import *
from copy import copy
from time import sleep, time

W = 10 ; H = 8 ; SS = 40
NUM_MINES = 10

class Game:
    def __init__(s):
        s.live = True
        s.started = False
        s.start_time = None
        s.b = {(coli,rowi): None for coli in range(W) for rowi in range(H)}
        s.mine_locs = None
        s.clicked = copy(s.b)
        s.flagged = copy(s.b)

        s.coords={}
        for coli, rowi in s.b.keys():
            x = coli*SS ; y = rowi*SS
            s.coords[(coli,rowi)] = (x,y)
            color = '#C8D8E4' if bool(coli%2==0) == bool(rowi%2==0) else '#A9BBCB'
            c.create_rectangle(x,y,x+SS,y+SS, fill=color, outline='')

    def get_loc(s,x,y):
        return x//SS,y//SS
    
    def get_touching_locs(s,loc):
        coli, rowi = loc
        offsets = [-1, 0, 1]
        touching_locs = [(coli + i, rowi + j) for i in offsets for j in offsets if (coli+i, rowi+j) in s.b.keys()]
        touching_locs.remove((coli,rowi))
        return touching_locs


    def get_screen(s): # for AI's benefit
        screen = {}
        for loc in s.b.keys():
            if s.clicked[loc]: # will be here even if that loc was expanded instead of clicked
                screen[loc] = s.b[loc]
            elif s.flagged[loc]:
                screen[loc] = 'f'
            else:
                screen[loc] = None
            
        return screen
    
    def set_up_board(s,click_loc):
        s.started = True
        s.start_time = time()
        placement_options = [loc for loc in s.b if not loc in s.get_touching_locs(click_loc) and not loc==click_loc]
        s.mine_locs = r.sample(placement_options, NUM_MINES)
        for loc in s.mine_locs:
            s.b[loc] = 'm'
        for loc in s.b:
            if not loc in s.mine_locs:
                touching_vals = [s.b[loc2] for loc2 in s.get_touching_locs(loc)]
                s.b[loc] = touching_vals.count('m')

    
    #Runs when a left click occurs, runs the start sequence if it is the first valid click
    def click(s,loc):
        if not loc in s.b.keys() or s.clicked[loc]:
            return
        
        if not s.started:
            s.set_up_board(loc)

        if s.b[loc] == 'm':
            s.explode_mines(loc)
            return
            
        if not s.clicked[loc]:
            x = s.coords[loc][0] + SS/2
            y = s.coords[loc][1] + SS/2
            s.clicked[loc]=c.create_text(x, y, text=s.b[loc], font = f'Helvetica {int(SS/2)}')
        if s.b[loc] == 0:
            s.expand(s.get_touching_locs(loc))

        s.check_for_win()
    
    def expand(s, to_do):
        new_to_do = set()
        for loc in to_do:
            x = s.coords[loc][0] + SS/2
            y = s.coords[loc][1] + SS/2
            s.clicked[loc]=c.create_text(x, y, text=s.b[loc], font = f'Helvetica {int(SS/2)}')
            if s.b[loc] == 0:
                new_to_do.update(s.get_touching_locs(loc))
        new_to_do = {loc for loc in new_to_do if not s.clicked[loc]}
        if new_to_do:
            s.expand(new_to_do)

    def flag(s,loc):
        coord = s.coords[loc]
        if s.flagged[loc]:
            c.delete(s.flagged[loc])
            s.flagged[loc] = None
        else:
            x = coord[0] ; y = coord[1]
            s.flagged[loc]=c.create_rectangle(x,y,x+SS,y+SS,fill='#FF6B6B',outline='')

    
    def check_for_win(s):
        opened = sum(1 for item in s.clicked.values() if item)
        if opened == W*H-NUM_MINES:
            s.live = False
            total_time = round(time() - s.start_time, 4)
            c.create_text((W*SS+10)/2, H*SS+35, text=f'Winner!    {total_time}s', font = 'Helvetica 20')


    def explode_mines(s,bad_click_loc):
        s.live = False
        # clicked mine will explode first
        s.mine_locs.remove(bad_click_loc)
        s.mine_locs.insert(0,bad_click_loc)
        for coli,rowi in s.mine_locs:
            x = coli*SS ; y=rowi*SS
            c.create_rectangle(x,y,x+SS,y+SS,fill='#80718C',outline='')
            tk.update()
            sleep(.25)

class AI:
    # not allowed to access values in s.game.b

    def __init__(s):
        s.game = Game()
        s.game.click(r.choice(list(s.game.b.keys())))


    # if a tile has the same amount of hidden squares around it as unflagged bombs remaining around it, then all the hidden tiles are bombs
    def mark_bombs(s):
        screen = s.game.get_screen()
        
        for loc in screen.keys():
            if not type(screen[loc]) is int:
                continue

            hidden_locs = [loc2 for loc2 in s.game.get_touching_locs(loc) if screen[loc2] is None]
            flagged_locs = [loc2 for loc2 in s.game.get_touching_locs(loc) if screen[loc2]=='f']
            if screen[loc]-len(flagged_locs) == len(hidden_locs):
                for to_flag_loc in hidden_locs:
                    s.game.flag(to_flag_loc)
                    screen = s.game.get_screen() # otherwise it may flag then unflag the same thing an even number of times
                        
    # if a tile has the same amount of flags around it as the number on the square, then all remaining hidden tiles around it aren't bombs
    def mark_not_bombs(s):
        screen = s.game.get_screen()
        for loc in screen.keys():
            hidden = [loc2 for loc2 in s.game.get_touching_locs(loc) if screen[loc2] is None]
            flagged = [loc2 for loc2 in s.game.get_touching_locs(loc) if screen[loc2]=='f']
            if screen[loc] == len(flagged):
                for to_click_loc in hidden:
                    s.game.click(to_click_loc)
                    screen = s.game.get_screen()

tk=Tk()
c = Canvas(tk, width=W*SS, height=H*SS+60)
c.pack()

ai = AI()

while ai.game.live:
    screen = ai.game.get_screen()
    tk.update() ; sleep(.25)
    ai.mark_bombs()
    tk.update() ; sleep(.25)
    ai.mark_not_bombs()

    if screen == ai.game.get_screen(): # not changed
        ai.mark_bombs() # if they aren't all already marked
        break

tk.mainloop()
'''
c.bind_all('<Left>', ai.mark_bombs)
c.bind_all('<Right>', ai.mark_not_bombs)
tk.mainloop()
'''