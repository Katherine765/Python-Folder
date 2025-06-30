# best this gets is about 27

from copy import copy
import random as r
from time import sleep

W = 10 ; H = 10 ; SHIPS = [2,3,3,4,5]
DIRECTIONS = [(1,0),(-1,0),(0,1),(0,-1)]

class Cell:
    def __init__(s):
        s.occupied = False
        s.char = ' '

class Battleship:
    def __init__(s):
        s.b = {(coli,rowi):Cell() for coli in range(W) for rowi in range(H)}
        s.rs = copy(SHIPS)
        s.rs_locs = []
        
        for ship in SHIPS:
            valid = False
            while not valid:
                locs = [(r.randint(0,W-1),r.randint(0,H-1))]
                direction = r.choice(DIRECTIONS)
                for _ in range(ship-1):
                    locs.append((locs[-1][0]+direction[0], locs[-1][1]+direction[1]))
                
                if all(loc in s.b and not s.b[loc].occupied for loc in locs):
                    valid = True   
            
            s.rs_locs.append(locs)
            for loc in locs:
                s.b[loc].occupied = True 

        s.count = 0
        s.live = True
        print('-'*W)

    def display(s):
        for rowi in range(H):
            for coli in range(W):
                print(s.b[(coli,rowi)].char, end='')
            print()
        print('-'*W)#,'\nTries:',s.count)
    
    def attack(s, loc):
        s.count += 1
        if s.b[loc].occupied:
            s.b[loc].char = 'X'
            return True
        else:
            s.b[loc].char = 'O'
            return False
        
    def check_sinkage(s, prog):
        for locs in s.rs_locs:
            if all(loc in prog for loc in locs):
                s.rs.remove(len(locs))
                s.rs_locs.remove(locs)
                return locs
        return []
    
    def update_liveness(s):
        if not s.rs:
            s.live = False
            print('Count: ', s.count)


class AI:
    def __init__(s):
        # {2: [range(-1, 1), range(0, 2)], 3: [range(-2, 1), range(-1, 2), range(0, 3)], 4: [range(-3, 1), range(-2, 2), range(-1, 3), range(0, 4)], 5: [range(-4, 1), range(-3, 2), range(-2, 3), range(-1, 4), range(0, 5)]} shows how a ship of a given size can be placed around cell 0 on a single axis.
        s.placement_ranges = {ship: [range(x, x+(ship-1)+1) for x in range(0-(ship-1), 0+1)] for ship in set(SHIPS)}
        s.all_prog = [] ; s.active_prog = [] ; s.prog_axis = None
        s.targeting = False

        s.g = Battleship()
        while s.g.live:
            loc = s.target() if s.targeting else s.search()
            if s.g.attack(loc):
                s.all_prog.append(loc) ; s.active_prog.append(loc)
                result = s.g.check_sinkage(s.active_prog)
                s.all_prog = [loc for loc in s.all_prog if not loc in result]
                s.active_prog = [loc for loc in s.active_prog if not loc in result]
                
                if not s.active_prog and s.all_prog:
                    s.active_prog = copy(s.all_prog)
                s.targeting = bool(s.active_prog)

            s.g.display()
            s.g.update_liveness()
            sleep(.7)


    def evaluate(s, loc, override=False):
        if not loc in s.g.b:
            return -9999,-9999
        if not override and s.g.b[loc].char != ' ':
            return -9999,-9999
        
        # map cross
        cross = {direction:0 for direction in DIRECTIONS}
        coli = loc[0] ; rowi = loc[1]
        for direction in DIRECTIONS:
            coli = loc[0]+direction[0] ; rowi = loc[1]+direction[1]
            while (coli,rowi) in s.g.b and s.g.b[(coli,rowi)].char == ' ':
                cross[direction] += 1
                coli += direction[0] ; rowi += direction[1]
        xrange = range(-cross[(-1,0)], cross[(1,0)]+1)
        yrange = range(-cross[(0,-1)], cross[(0,1)]+1)

        # get the scores
        xscore = 0 ; yscore = 0
        for ship in s.g.rs:
            for placement_range in s.placement_ranges[ship]:
                # adds boolean if this placement is possible given this cell's mapped cross
                xscore += all(x in xrange for x in placement_range)
                yscore += all(y in yrange for y in placement_range) 
        return xscore, yscore


    def target(s):
        if len(s.active_prog)==1:
            xscore, yscore = s.evaluate(s.active_prog[0], override=True)
            s.prog_axis = 'x' if xscore >= yscore else 'y'

        if s.prog_axis == 'x':
            s.active_prog = sorted(s.active_prog, key = lambda x: x[0])
            loc_options = [(coli,s.active_prog[0][1]) for coli in (s.active_prog[0][0]-1, s.active_prog[-1][0]+1)]
        else:
            s.active_prog = sorted(s.active_prog, key = lambda x: x[1])
            loc_options = [(s.active_prog[0][0],rowi) for rowi in (s.active_prog[0][1]-1, s.active_prog[-1][1]+1)]
        scores = {loc: sum(s.evaluate(loc)) for loc in loc_options}


        max_score = max(scores.values())
        if max_score >= 0: # will be 0 if that square is clear but not any next to it are
            return next(loc for loc, score in scores.items() if score == max_score)
        else:
            s.active_prog = [s.all_prog[0]]
            return s.target()


    def search(s):
        best_score = 0
        best_loc = None
        for loc in s.g.b.keys():
            if not s.g.b[loc].char == ' ':
                continue
            score = sum(s.evaluate(loc))
            if score > best_score:
                best_score = score
                best_loc = loc
        return best_loc


ai = AI()
# avg: 43.76, good
