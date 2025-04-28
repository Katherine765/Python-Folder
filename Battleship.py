from copy import copy, deepcopy
from itertools import chain
from time import sleep
from random import choice, randint, shuffle

# disclaimer bot is told exactly where the ship it sunk is
# confirmed every turn it is doing something
# maybe when targeting if two sides have the same axis score, see which has the better total score?

H = 10
W = 10

converter = {0:' ', 1: '-', 2:'O', 3:'X'}
def print_b(b):
    for rowi in range(H):
        row = [converter[b[coli][rowi]] for coli in range(W)]
        print(*row,'|', sep='')
    print('-'*W)

def generate_sb(ships):
    sb = deepcopy(blank_grid)
    sl = []
    while ships:
        # start a new ship
        valid = True
        coords = [(randint(0,W-1),randint(0,H-1))] # endpoints are inclusive
        direction = choice(directions)
        # finish creating that ship
        for _ in range(1, ships[-1]):
            coli = coords[-1][0]+direction[0]
            rowi = coords[-1][1]+direction[1]
            if coli not in range(W) or rowi not in range(H) or sb[coli][rowi]:
                valid = False
                break
            coords.append((coli, rowi))

        if valid:
            ships.pop()
            sl.append(coords)
            for coord in coords:
                sb[coord[0]][coord[1]] = 1
    return sb, sl
        
def map_cross(coli, rowi, pb, rs):
    mapped_cross = [0,0,0,0]
    
    # right
    range_endpoint = min(W, coli+max(rs)) # still need this part bc prog_cross relies on limited cross lengths
    for x in range(coli+1, range_endpoint):
        if pb[x][rowi]:
            break
        mapped_cross[0] += 1
    
    # left
    range_endpoint = -max(-1, coli-max(rs)) # -1 bc exclusive, i think this was the last pub
    for x in range(coli-1, range_endpoint, -1):
        if pb[x][rowi]:
            break
        mapped_cross[1] += 1

    # up
    range_endpoint = min(H, rowi+max(rs))
    for x in range(rowi+1, range_endpoint):
        if pb[coli][x]:
            break
        mapped_cross[2] += 1
    
    # down
    range_endpoint = max(-1, rowi-max(rs))
    for x in range(rowi-1, range_endpoint, -1):
        if pb[coli][x]:
            break
        mapped_cross[3] += 1

    return mapped_cross

#i feel like these two functions should be working
def value_cell(coli,rowi,pb,rs):
    if not coli in range(W) or not rowi in range(H):
        return 0,0
    if pb[coli][rowi]:
        return 0,0
    
    horiz_val = 0
    vert_val = 0
    mapped_cross = map_cross(coli,rowi, pb, rs)
    for s in rs:
        reduced_cross = [min(length, s-1) for length in mapped_cross]
        horiz_val += (reduced_cross[0]+reduced_cross[1]+1) -s+1
        vert_val += (reduced_cross[2]+reduced_cross[3]+1) -s+1
    return horiz_val, vert_val
    

def make_vg(pb, rs):
    vg = deepcopy(blank_grid)
    for coli in range(W):
        for rowi in range(H):
            vg[coli][rowi] = sum(value_cell(coli,rowi,pb,rs))
    if all(not value for value in list(chain(*vg))):
           print('no square has any value')
    return vg


def search(pb, rs):
    vg = make_vg(pb, rs)
    unnested_vg = list(chain(*vg))
    shot = unnested_vg.index(max(unnested_vg))
    converted_shot = (shot//H,shot%H)
    return converted_shot


def target(pb, rs):
    global progress ; global prog_cross ; global prog_dir
    if len(progress) == 1:
        coli = progress[0][0]
        rowi = progress[0][1]

        pb_sans_hit = deepcopy(pb)
        pb_sans_hit[coli][rowi] = 0
        points = []
        for direction in directions:
            # only cares about the axis aligned with the hit
            axis = 0 if direction[0] else 1
            # might get an extra point for an orientation in the correct axis not including the hit
            points.append(value_cell(coli+direction[0],rowi+direction[1], pb_sans_hit, rs)[axis])
        direction = directions[points.index(max(points))]              
        prog_dir = sorted([direction, (-direction[0],-direction[1])], reverse = True) # forward then backward
        mapped_cross = map_cross(coli,rowi,pb, rs)
        prog_cross = [mapped_cross[directions.index(prog_dir[0])], mapped_cross[directions.index(prog_dir[1])]]

    # dealing w/ mult ships
    if prog_cross == [0,0]:
        progress = start_progress(pb)
        return target(pb, rs)
        
        
    progress = sorted(progress, reverse=True)
    max_i = prog_cross.index(max(prog_cross))
    direction = prog_dir[max_i]

    # expand in more expandable direction and update cross accordingly
    prog_cross[max_i] -= 1
    if 1 in direction: # if going forward
        return (progress[0][0]+direction[0], progress[0][1]+direction[1]), max_i
    else:
        return (progress[-1][0]+direction[0], progress[-1][1]+direction[1]), max_i
    
def start_progress(pb):
    for coli, col in enumerate(pb):
        for rowi, row in enumerate(col):
            if pb[coli][rowi] == 2:
                return [(coli, rowi)]
    # no started ships
    return []


blank_grid = [[0 for i in range(W)] for ii in range(H)] # list of columns
directions = [(1,0), (-1,0), (0,1), (0,-1)] # right left up down

# remaining ships, solved board, ship locations, pegged board, value grid
rs = [2,3,3,4,5]
sb, sl = generate_sb(copy(rs))
pb = deepcopy(blank_grid)

global progress ; global prog_cross ; global prog_dir
progress = [] # cells found in targeting ship
prog_cross = [] # ok so its not really a cross
prog_dir = []


print_b(sb)
while rs:
    if progress:
        print('targeting')
        shot, max_i = target(pb, rs)
    else:
        print('searching')
        shot = search(pb, rs)
        
    landing = sb[shot[0]][shot[1]]
    if landing:
        pb[shot[0]][shot[1]] = 2
    else:
        pb[shot[0]][shot[1]] = 1
        if progress:
            prog_cross[max_i] = 0
    
    if landing:
        progress.append((shot[0],shot[1]))
        for ship in sl:
            if all(pb[coord[0]][coord[1]] for coord in ship):
                for coord in ship:
                    pb[coord[0]][coord[1]] = 3
                rs.remove(len(ship))
                sl.remove(ship)

                progress = start_progress(pb)

    print_b(pb)

guesses = 0
for cell in list(chain(*pb)):
    if cell:
        guesses += 1
print(guesses)
