# inefficient but works
#if the program starts with multiple of the same color touching, i need to add those to the blob

from random import choice
from tkinter import *
from itertools import chain

colors = ["#FFC08A", "#A2FFB1", "#A7B6FF", "#FFA6D8",\
          "#FFF48D", "#8DF5F5", "#FF8F9B", "#D4A6FF"]
width = 14
height = 14
square_size = 30

class Game():
    def __init__(s, num_colors, tries):
        s.colors = colors[:num_colors]
        s.total_tries = tries
        s.used_tries = 0
        s.text = canvas.create_text((width*square_size+10)/2, height*square_size+35, text=f'{s.used_tries}/{s.total_tries}', font='Helvetica 20')

        s.grid = {(x,y): choice(s.colors) for x in range(width) for y in range(height)}
        s.coords = {loc:((loc[0]*square_size + 5), (loc[1]*square_size + 5)) for loc in s.grid.keys()}
        s.squares = {}

        for loc in s.grid.keys():
            s.update(loc)

        s.blob = [(0,0)]
        s.current_color = s.grid[(0,0)]

            
    def touching_locs(s,loc):
        x = loc[0] ; y = loc[1]
        touching = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return [loc for loc in touching if loc in s.grid.keys()]

    def update(s,loc):
            if loc in s.squares: #this only isn't true on the first run
                canvas.delete(s.squares[loc])
            x = s.coords[loc][0]
            y = s.coords[loc][1]
            s.squares[loc] = canvas.create_rectangle(x,y,x+square_size,y+square_size, fill = s.grid[loc], outline = '')

    def get_square_loc(s,x,y):
        return (x-5)//square_size,(y-5)//square_size
 
    def flood(s,event):
        s.used_tries += 1
        
        clickx = event.x
        clicky = event.y
        loc = s.get_square_loc(clickx,clicky)
        s.current_color = s.grid[loc]
        
        for loc in s.blob:
            s.grid[loc] = s.current_color
            s.update(loc)
            
        to_do = list(chain(*[s.touching_locs(loc2) for loc2 in s.blob]))
        s.expand(to_do)

        s.end_of_turn()
              

    def expand(s,to_do):
        to_do = set([loc for loc in to_do if not loc in s.blob])
        new_to_do = set()
        for loc in to_do:
            if s.grid[loc] == s.current_color:
                s.blob.append(loc)
                new_to_do.update(s.touching_locs(loc))
        if new_to_do:
            s.expand(new_to_do)
        else:
            return

    def end_of_turn(s):
        canvas.delete(s.text)
        s.text = canvas.create_text((width*square_size+10)/2, height*square_size+35, text=f'{s.used_tries}/{s.total_tries}', font='Helvetica 20')
        if len(s.blob) == width*height:
            print('winner')
            canvas.unbind_all('<Button-1>')
        elif s.used_tries == s.total_tries:
            print('loser')
        


tk = Tk()
canvas = Canvas(tk, width=width*square_size+10, height=height*square_size+60)
canvas.pack()

g = Game(6,25)
canvas.bind_all('<Button-1>', g.flood)
