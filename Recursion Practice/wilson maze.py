# top left is (0,0)
# maybe make this a class?

from random import choice

symbols={('L','R'):'─',('D','U'):'│',('D','R'):'┌',('D','L'):'┐',('R','U'):'└',('L','U'):'┘',('L','R','U'):'┴',('D','L','R'):'┬',('D','L','U'):'┤',('D','R','U'):'├',('D','L','R','U'):'┼',('L',):'─',('R',):'─',('D',):'│',('U',):'│'}#('L',):' ',('R',):' ',('D',):' ',('U',):' '}#('L',):'╸',('R',):'╺',('D',):'╻',('U',):'╹'}

W = 30 ; H = 20
CELLS = {(x,y) for x in range(W) for y in range(H)}
paths = [[(W-1,H-1)],[]]

def get_touching_cells(cell):
    x, y = cell
    maybes =  {(x+1, y), (x-1, y), (x, y+1), (x, y-1)}
    return maybes & CELLS
def get_new_start():
    options = CELLS - {cell for path in paths for cell in path}
    return choice(list(options)) if options else None

def get_direction(cell,neighbor): 
    if neighbor[0] - cell[0] > 0:
         return 'R'
    elif neighbor[0] - cell[0] < 0:
        return 'L'
    elif neighbor[1] - cell[1] > 0:
        return 'D'
    return 'U'
     
#print(get_direction((0,0),(0,1)))

def display(): # displays paths
    directions = {cell:[] for cell in CELLS}
    for path in paths:
        for i, cell in enumerate(path):
            if i > 0:
                directions[cell].append(get_direction(cell, path[i-1]))
            if i < len(path)-1:
                directions[cell].append(get_direction(cell, path[i+1]))
    chosen_symbols = {cell:symbols[tuple(sorted(directions[cell]))] for cell in CELLS}

    for y in range(H):
        for x in range(W):
            print(chosen_symbols[(x,y)], end='')
        print()        
               

# generates one path then calls to make another
def generate():
    used_cells = {cell for path in paths for cell in path}

    current = get_new_start()
    if len(paths)==2:
        current = (0, 0)
    if not current:
         return # BASE CASE
    paths[-1].append(current)

    path_complete = False
    while not path_complete:
        options = get_touching_cells(current)
        if len(paths[-1]) > 1:
            options.remove(paths[-1][-2])
        current = choice(list(options))
        if current in used_cells:
             paths[-1].append(current) # to be used to determine direction of last line
             paths.append([])
             path_complete = True
        elif current in paths[-1]:
             paths[-1] = paths[-1][:paths[-1].index(current)+1]
        else:
             paths[-1].append(current)

    generate()   

generate()
display()