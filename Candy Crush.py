# x and y for coords, coli and rowi for locs

# need to update moves text more frequently

from copy import copy
from itertools import chain
import random as r
from time import sleep
from tkinter import *
import requests

url = 'https://www.schemecolor.com/the-bold-and-the-bright.php'
#url = 'https://www.schemecolor.com/elite-maroon-blue-and-gold.php'
content = str(requests.get(url).content)
colors = content[content.find('#'):content.find('. This')]
colors = colors.replace(' and', ',').split(', ')


'''colors = ["#FFC08A", "#A2FFB1", "#A7B6FF", "#FFA6D8",\
          "#FFF48D", "#8DF5F5", "#FF8F9B", "#D4A6FF"]'''
#colors = ['#3D3D6B', '#79C7C9', '#FCE7A6', '#FC6F9D', '#9358B0'] #webscraped

W = 10 ; H = 10 ; SS = 50 ; num_colors = 5 ; pause = .75 ; streak_color = "#A4A1A2" # or linen
colors = colors[:num_colors]

class Game:
    def __init__(s):
        s.b = {(coli,rowi): r.choice(colors) for coli in range(W) for rowi in range(H)}
        s.coords = {loc:(loc[0]*SS+5, loc[1]*SS+5) for loc in s.b.keys()}
        s.squares = {loc:None for loc in s.b.keys()}
        s.prev_coli = None ; s.prev_rowi = None

        s.score = 0
        s.moves = 0
        s.text = c.create_text((W*SS+10)/2, H*SS+35, text=f'Score: {s.score}    Moves: {s.moves}', font='Saab 18')
        for loc, c_item in s.squares.items():
            x, y = s.coords[loc]
            s.squares[loc] = c.create_rectangle(x,y,x+SS,y+SS, fill=s.b[loc], outline = '', width  = 5)
        
        s.outline = None
        s.remove_streaks()
        
    def get_i(s,x_or_y): # get coli or rowi
        return (x_or_y-5)//SS
    def get_col(s,coli): #working
        return [s.b[(coli,rowi)] for rowi in range(H)]
    def get_row(s,rowi): #working
        return [s.b[(coli,rowi)] for coli in range(W)]
    def update(s):
        for loc, c_item in s.squares.items():
            c.itemconfig(s.squares[loc],fill=s.b[loc])

        c.delete(s.text)
        s.text = c.create_text((W*SS+10)/2, H*SS+35, text=f'Score: {s.score}    Moves: {s.moves}', font='Saab 18')
    def gray(s, to_gray):
        for loc in to_gray:
            c.itemconfig(s.squares[loc],fill=streak_color)
    def display_outline(s,loc):
        width = 3
        x, y = s.coords[loc]
        s.outline = c.create_rectangle(x+2,y+2,x+SS-3,y+SS-3,fill='',outline='#333333',width=5)

    def click(s,e):
        coli = s.get_i(e.x)
        rowi = s.get_i(e.y)

        # no trying to swap with blanks
        if not s.b[(coli,rowi)]:
            print("nope")
            return
        
        if None in (s.prev_coli,s.prev_rowi): # if one exists the other does too but maybe this helps w/ rEaDaBiLiTy
            s.display_outline((coli,rowi))
            s.prev_coli = coli
            s.prev_rowi = rowi
            
        else:
            s.moves += 1
            c.delete(s.outline)
            
            # if the squares are next to each other
            if {abs(s.prev_coli-coli), abs(s.prev_rowi-rowi)} == {0,1}:
                temp = copy(s.b[(coli,rowi)])
                s.b[(coli,rowi)] = copy(s.b[(s.prev_coli, s.prev_rowi)])
                s.b[(s.prev_coli, s.prev_rowi)] = copy(temp)

                s.update()
                tk.update()
                sleep(pause)
                s.remove_streaks() # kicks off seq of removing, collapsing, refilling

            s.prev_coli = None
            s.prev_rowi = None
            

    #working
    def get_streak_is(s,full): # i for indexes, and its plural
        streaks = []
        prev_color = None
        for i, color in enumerate(full):
            if not color:
                prev_color = None
                continue
            # continue current streak
            if color == prev_color:
                streaks[-1].append(i)
            # start new streak                
            else:
                streaks.append([i])
                prev_color = color
        return list(chain(*[streak for streak in streaks if len(streak)>2])) # indexes that are part of a streak

    def remove_streaks(s,rowis=range(H),colis=range(W)):
        colis_to_collapse = set()
        new_b = s.b.copy() # so not changing something that changes are based on
        to_gray = set()

        # set none to where all the streaks are in the current board
        for rowi in rowis:
            for coli in s.get_streak_is(s.get_row(rowi)):
                new_b[(coli,rowi)] = None
                colis_to_collapse.add(coli)
                to_gray.add((coli,rowi))
        for coli in colis:
            for rowi in s.get_streak_is(s.get_col(coli)):
                new_b[(coli,rowi)] = None
                colis_to_collapse.add(coli)
                to_gray.add((coli,rowi))

        s.b = new_b.copy()
        if colis_to_collapse:
            s.gray(to_gray)
            tk.update()
            sleep(pause)
            s.collapse_and_refill(colis_to_collapse)
    
    def collapse_and_refill(s, colis):
        for coli in colis:
            col = s.get_col(coli)
            collapsed_col = [color for color in col if color]
            refilled_col = copy(collapsed_col)
            for i in range(H-len(collapsed_col)):
                refilled_col.insert(0,r.choice(colors))
                s.score += 1

            for rowi, color in enumerate(refilled_col):
                s.b[(coli,rowi)] = color

        s.update()
        tk.update()
        sleep(pause)
        s.remove_streaks()


tk = Tk()
c = Canvas(tk, width=W*SS+10, height=H*SS+10+60)
c.pack()
g = Game()
c.bind_all('<Button-1>', g.click)
mainloop()