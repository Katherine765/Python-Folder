import random as r
from tkinter import *
from time import sleep
from copy import copy, deepcopy as dc
from Tetromino import Tetromino

W = 10 ; H = 15+4 ; SS = 30
shape_names = ('i','j','l','o','z','t','s')

class Tetris():
    def __init__(s):
        s.live = True
        s.b = {(x,y): 'black' for x in range(W) for y in range(H)}
        s.tetromino = None
        s.score = 0
    
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
        return True
        

    def draw_start(s):
        s.spawn()

        s.score_text = c.create_text((W*SS+10)/2, H*SS+35, text=str(s.score), font='Helvetica 20')
        s.squares = {loc:None for loc in s.b.keys()}
        for loc in s.b.keys():
            x = loc[0]*SS ; y = loc[1]*SS
            s.squares[loc] = c.create_rectangle(x,y,x+SS,y+SS, fill=s.b[loc], outline = '')


    def draw(s):
        c.itemconfig(s.score_text, text=s.score)
        for loc in s.b.keys():
            c.itemconfig(s.squares[loc], fill=s.b[loc])

    def spawn(s):
        s.tetromino = Tetromino(r.choice(shape_names))
        for loc in s.tetromino.locs:
            s.b[loc] = s.tetromino.color


    def slam(s):
        move_successful = True
        while move_successful:
            move_successful = s.move('down')

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


    def get_move_validity(s, new_locs):
        for loc in new_locs:
            if not loc in s.b:
                return False
            if not s.b[loc] == 'black' and not loc in s.tetromino.locs:
                return False  
        return True


class AI():
    def __init__(s):
        s.game = Tetris()
        s.game.draw_start()

    def score_board(s, board):
        # a combined height, b rows cleared, c holes, d bumpiness, #e amount above holes (e was the only one i came up with)
        a,c,d,e = 0,0,0,0
        b = (list(board.values()).count('black')-list(s.game.b.values()).count('black'))/10
        penalty = False
        prev_col = None
        for coli in range(W):
            col = [board[(coli,rowi)] for rowi in range(H)]
            while col and col[0] == 'black':
                del col[0]
            if len(col) > H-4:
                penalty = True
            a += len(col)
            
            if 'black' in col:
                c += col.count('black')
                e += sum(1 for rowi in range(col.index('black'), len(col)) if board[(coli,rowi)] != 'black')

            if prev_col:
                d += abs(len(col)-len(prev_col))
            prev_col = copy(col)
        return -8*a+5*b-3*c-1.5*d-99999999*penalty #-1*e # treating bool like int :)

    def move(s):
        test_game = dc(s.game)
        test_game.slam()
        best_score = s.score_board(test_game.b) # sets original score to beat w/ no turn or sliding
        best_game = test_game

        num_turns = 0
        turn_successful = True
        base_turned_game = dc(s.game)
        while turn_successful and num_turns < s.game.tetromino.num_orientations:
            for slide_type in ('left','right'):
                slide_successful = True
                slid_game = dc(base_turned_game)
                while slide_successful:
                    test_game = dc(slid_game)
                    test_game.slam()
                    score = s.score_board(test_game.b)
                    if score > best_score:
                        best_score = score
                        best_game = dc(test_game)
                    
                    slide_successful = slid_game.move(slide_type)
                
            turn_successful = base_turned_game.move('turn')
            num_turns += 1
        
        s.game = best_game
        if s.game.live:
            s.game.spawn()
        s.game.draw()


tk=Tk()
c = Canvas(tk, width=W*SS, height=H*SS+50)
c.pack()

ai = AI()
while ai.game.live: 
    ai.move()
    tk.update()

sleep(3)    
print('done')
