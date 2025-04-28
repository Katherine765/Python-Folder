from random import choice
W = 45
H = 15

grid = {(coli,rowi):'█' for coli in range(W) for rowi in range(H)}

def get_touching_locs(loc):
        coli, rowi = loc
        return [(coli-1, rowi), (coli+1, rowi), (coli, rowi+1), (coli, rowi-1)]
        offsets = [-1, 0, 1]
        touching_locs = [(coli+i, rowi+j) for i in offsets for j in offsets]
        touching_locs.remove((coli,rowi))
        return touching_locs

def get_options(loc):
    coli = loc[0]
    rowi = loc[1]
    potential = [(coli-1, rowi), (coli+1, rowi), (coli, rowi+1), (coli, rowi-1)]
    potential = [option for option in potential if option in grid and grid[option]=='█']

    options = []
    for loc2 in potential:
        touching = get_touching_locs(loc2)
        for loc3 in touching:
            if not loc3 in grid or (grid[loc3] == ' ' and not loc3==loc):
                break
        else:
            options.append(loc2)

    return options


def display():
    for rowi in range(H):
        for coli in range(W):
            print(grid[(coli,rowi)], end='')
        print()
    

def generate(start):
    while True:
        options = get_options(start)
        if not options:
            return
        
        nextt = choice(options)
        grid[nextt] = ' '
        generate(nextt)

grid[(1,1)] = ' '
generate((1,1))
display()
