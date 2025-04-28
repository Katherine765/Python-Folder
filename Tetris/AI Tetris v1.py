import random as r
from tkinter import *
from copy import copy, deepcopy
from Tetromino import Shape
from time import sleep

#465 rows cleared - pretty darn good

W = 10 ; H = 15+4 ; SS = 30
shape_names = ('i','j','l','o','z','t','s')

class Game():
    def __init__(s):
        s.live = True
        s.b = {(x,y): 'black' for x in range(W) for y in range(H)}
        s.curr_shape = None
        s.score = 0
    
    def replace_curr_shape(s, shape):
        for loc in s.curr_shape.locs:
            s.b[loc] = 'black'
        
        s.curr_shape = shape
        for loc in s.curr_shape.locs:
            s.b[loc] = s.curr_shape.color


    def draw_start(s):
        s.score_text = c.create_text((W*SS+10)/2, H*SS+35, text=str(s.score), font='Helvetica 20')
        s.squares = {loc:None for loc in s.b.keys()}
        for loc in s.squares.keys():
            x = loc[0]*SS ; y = loc[1]*SS
            s.squares[loc] = c.create_rectangle(x,y,x+SS,y+SS, fill=s.b[loc], outline = '')
        s.spawn()
        s.draw()

    def draw(s):
        c.delete(s.score_text)
        s.score_text = c.create_text((W*SS+10)/2, H*SS+35, text=str(s.score), font='Helvetica 20')
        for loc in s.b.keys():
            c.itemconfig(s.squares[loc], fill=s.b[loc])

    def spawn(s):
        s.curr_shape = Shape(r.choice(shape_names))
        for loc in s.curr_shape.locs:
            s.b[loc] = s.curr_shape.color


    def slam(s):
        new_locs = copy(s.curr_shape.locs)
        while s.get_move_validity(new_locs):
            new_locs = [(coli,rowi+1) for coli,rowi in new_locs]
        new_locs = [(coli,rowi-1) for coli,rowi in new_locs] #one too far in loop

        for loc in s.curr_shape.locs:
            s.b[loc] = 'black'
        s.curr_shape.locs = new_locs # don't worry abt references bc it won't move again
        for loc in s.curr_shape.locs:
            s.b[loc] = s.curr_shape.color

        s.land_sequence()


    def get_move_validity(s, new_locs):
        for loc in new_locs:
            if not loc in s.b:
                return False
            if not s.b[loc] == 'black' and not loc in s.curr_shape.locs:
                return False  
        return True

    def land_sequence(s):
        top_rowi = min([loc[1] for loc, color in s.b.items() if color != 'black'])

        # deletes the full rows. rowi is the full row, rowi2 is the ones above
        for full_rowi in range(top_rowi, H):
            if 'black' in (s.b[(coli, full_rowi)] for coli in range(W)):
                continue
            s.score += 1

            row_locs = [(coli, full_rowi) for coli in range(W)]

            for loc in row_locs:
                s.b[loc] = 'black'

            rowis_to_move = [rowi for rowi in range(top_rowi, H) if rowi < full_rowi]
            to_move = [(coli,rowi) for rowi in rowis_to_move for coli in range(W)]

            for coli,rowi in reversed(to_move):
                s.b[(coli, rowi+1)] = s.b[(coli,rowi)]
                s.b[(coli, rowi)] = 'black'

            top_rowi += 1    

        if min([loc[1] for loc, color in s.b.items() if color != 'black']) < 4:
            s.live = False
    


class AI():
    def __init__(s):
        s.game = Game()
        s.game.draw_start()

    def score_board(s, board):
        a,c,d = 0,0,0
        b = (list(board.values()).count('black')-list(s.game.b.values()).count('black'))/10
        penalty = False
        prev_col = None
        for coli in range(W):
            col = [board[(coli,rowi)] for rowi in range(H)]
            while col and col[0] == 'black':
                del col[0]
            if len(col) > H-4:
                penalty = True
                print('penalty')
            a += len(col)
            c += col.count('black')
            if prev_col:
                d += abs(len(col)-len(prev_col))
            prev_col = copy(col)
        return -.79875*a+.522287*b-.249214*c-.164626*d - 9999*penalty #yes im treating a boolean like an integer

    # lookin good
    def get_moveseqs(s):
        moveseqs = [deepcopy(s.game.curr_shape)]
        counter = 0
        shape = deepcopy(s.game.curr_shape)
        while s.game.get_move_validity(shape.locs) and counter < s.game.curr_shape.num_orientations:
            counter += 1
            shape.turn()
            moveseqs.append(deepcopy(shape)) #new  
        counter -= 1
        del moveseqs[-1]

        #moveseqs = [i*['turn']+['down'] for i in range(counter)]
        for num_turns in range(counter+1):
            shape = deepcopy(s.game.curr_shape)
            for _ in range(num_turns):
                shape.turn()
            
            for slide_type in ('left','right'):
                shape2 = deepcopy(shape)
                slide_method = getattr(shape2, slide_type)
                num_slides = 0
                while s.game.get_move_validity(shape2.locs):
                    num_slides += 1
                    slide_method()
                    #moveseqs.append(num_turns*['turn']+num_slides*[slide_type]+['down'])
                    moveseqs.append(deepcopy(shape2))

                del moveseqs[-1]

        return moveseqs

    def choose_moveseq(s):

        #return r.choice(s.get_moveseqs())
        best_score = -float('inf')
        best_shape = None # will take the shape, replace the curr shape, then slam
        moveseqs = s.get_moveseqs() # bad naming
        for shape in moveseqs:
            test_game = deepcopy(s.game)
            test_game.replace_curr_shape(shape)
            test_game.slam()
            score = s.score_board(test_game.b)
            if score > best_score:
                best_score = score
                best_shape = deepcopy(shape)

        return best_shape
    
    def move(s):
        shape = s.choose_moveseq()
        s.game.replace_curr_shape(shape)
        s.game.slam()
        
        s.game.draw()
        if s.game.live:
            s.game.spawn()


tk=Tk()
c = Canvas(tk, width=W*SS, height=H*SS+50)
c.pack()

ai = AI()
while ai.game.live: 
    ai.move()
    tk.update()
    sleep(.1)
    
print('done')
tk.mainloop()