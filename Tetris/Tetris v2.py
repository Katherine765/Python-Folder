import random as r
from tkinter import *
from time import sleep
from copy import deepcopy as dc
from Tetromino import Tetromino

W = 10 ; H = 15+4 ; SS = 30
shape_names = ('i','j','l','o','z','t','s')

class Tetris():
    def __init__(s):
        s.live = True
        s.b = {(x,y): 'black' for x in range(W) for y in range(H)}
        s.tetromino = None
        s.score = 0
        s.score_text = c.create_text((W*SS+10)/2, H*SS+35, text=str(s.score), font='Helvetica 20')
        s.squares = {loc:None for loc in s.b.keys()}
        for loc in s.b.keys():
            x = loc[0]*SS ; y = loc[1]*SS
            s.squares[loc] = c.create_rectangle(x,y,x+SS,y+SS, fill=s.b[loc], outline = '')

        s.spawn()
        s.fall_constant()
    
    def move(s, direction):
        new = dc(s.tetromino)
        getattr(new, direction)()
        if not s.get_move_validity(new.locs):
            return False

        for loc in s.tetromino.locs:
            s.b[loc] = 'black'
        s.tetromino = new
        for loc in s.tetromino.locs:
            s.b[loc] = s.tetromino.color

        s.draw()
        return True

    def spawn(s):
        s.tetromino = Tetromino(r.choice(shape_names))
        for loc in s.tetromino.locs:
            s.b[loc] = s.tetromino.color

        s.draw()


    def slam(s, e):
        move_successful = True
        while move_successful:
            move_successful = s.move('down')
        s.land()

    def land(s):
        # clears full rows
        top_rowi = min([loc[1] for loc, color in s.b.items() if color != 'black'])
        for full_rowi in range(top_rowi, H):
            if 'black' in (s.b[(coli, full_rowi)] for coli in range(W)):
                continue
            s.score += 1

            for coli in range(W): 
                s.b[(coli,full_rowi)] = 'black'

            # moves everything down 1
            for rowi in reversed(range(top_rowi, full_rowi)):
                for coli in range(W):
                    s.b[(coli, rowi+1)] = s.b[(coli,rowi)]
                    s.b[(coli, rowi)] = 'black'

        for x in range(W):
            for y in range(4):
                if s.b[(x,y)] != 'black':
                    s.live = False
                    c.unbind_all()
                    c.unbind_all('<Down>') 
                    c.unbind_all('<Up>')
                    c.unbind_all('<Left>') 
                    c.unbind_all('<Right>')
                    return
        s.spawn()

    def draw(s):
        c.itemconfig(s.score_text, text=s.score)
        for loc in s.b.keys():
            c.itemconfig(s.squares[loc], fill=s.b[loc])

    # stupid implementation
    def fall_constant(s):
        s.move('down')

        test = dc(s.tetromino)
        test.down()
        if not s.get_move_validity(test.locs):
            s.land()


        tk.after(250, s.fall_constant)

    def get_move_validity(s, new_locs):
        for loc in new_locs:
            if not loc in s.b:
                return False
            if not s.b[loc] == 'black' and not loc in s.tetromino.locs:
                return False
        return True


tk=Tk()
c = Canvas(tk, width=W*SS, height=H*SS+50)
c.pack()

game = Tetris()
c.bind_all('<Down>', game.slam)
c.bind_all('<Up>', lambda e: game.move('turn'))
c.bind_all('<Left>', lambda e: game.move('left'))
c.bind_all('<Right>', lambda e: game.move('right'))

tk.mainloop()