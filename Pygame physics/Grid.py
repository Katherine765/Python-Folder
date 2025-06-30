# could add to grid: rotate, transpose, mirror
# everyhting on here *should* be working
from math import copysign

# still assumes SS, so idk why this'd be used w/o pg or tkinter
class Grid(dict):
    # can pass a fully completed dict, a partially completed dict with a value func to finish the values, a partially completed dict with a default None to finish the values, an empty dict with a value func to fill all the values, or an empty dict with a default None for all the values
    def __init__(s, nCols, nRows, items={}, valueFunc= lambda _: None, SS=50, offsetX = 0, offsetY = 0):
        for coli in range(nCols):
            for rowi in range(nRows):
                if not (coli,rowi) in items.keys():
                    items[(coli,rowi)] = valueFunc((coli,rowi))
        super().__init__(items)
        s.nCols = nCols ; s.nRows = nRows ; s.SS = SS
        s.offsetX = offsetX ; s.offsetY = offsetY
    def getWinDimensions(s):
        return s.nCols*s.SS, s.nRows*s.SS
    def getLoc(s, x, y):
        return int((x+s.offsetX)//s.SS),int((y+s.offsetY)//s.SS)
    def getCornerCoords(s, loc):
        return loc[0]*s.SS+s.offsetX, loc[1]*s.SS+s.offsetY
    def getCenterCoords(s, loc):
        x, y = s.getCornerCoords(loc)
        return int(x+s.SS/2), int(y+s.SS/2)
    def getNeighbors(s,loc):
        coli, rowi = loc
        offsets = [-1, 0, 1]
        touching = [(coli+i, rowi+j) for i in offsets for j in offsets if (coli+i, rowi+j) in s]
        touching.remove((coli,rowi))
        return touching
    def getCardinalNeighbors(s, loc):
        coli, rowi = loc
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        touching = [(coli+dx, rowi+dy) for dx, dy in offsets if (coli+dx, rowi+dy) in s]
        return touching
    def display(s, w=None, charFunc= lambda x: x, border=False):
        if not w:
            # longest after processing
            w = max(len(str(charFunc(val))) for val in s.values())
        if border:
            print('-'*(w*s.nCols+2))
        for rowi in range(s.nRows):
            if border:
                print('|', end='')
            for coli in range(s.nCols):
                text = str(charFunc(s[(coli,rowi)]))[:w]
                print(f'{text:<{w}}', end='') # add spaces to make the right width
            print('|' if border else '')
        if border:
            print('-'*(w*s.nCols+2))
    def setLocs(s, locs, val=None):
        for loc in locs:
            s[loc] = val
    def floodFill(s, loc, val):
        if s[loc] == val:
            return s
        s[loc] = val
        coli, rowi = loc
        for (coli2, rowi2) in [(coli+1, rowi), (coli-1, rowi), (coli, rowi+1), (coli, rowi-1)]:
            if (coli2, rowi2) in s:
                s.floodFill((coli2,rowi2), val)

    def checkSightBetween(s, loc1, loc2, obstacle = lambda val: bool(val)):
        x1, y1 = s.getCenterCoords(loc1)
        x2, y2 = s.getCenterCoords(loc2)
        rise = y2-y1 ; run = x2-x1
        xStep = int(copysign(3, x2 - x1)) if x2 != x1 else 0
        if xStep:
            yStep = xStep * rise / run
            rangee = range(0, run, xStep)
        else:
            yStep =  int(copysign(3, y2 - y1))
            rangee = range(0, rise, yStep)
        for _ in rangee:
            x1 += xStep
            y1 += yStep
            if obstacle(s[s.getLoc(x1,y1)]):
                return False
        return True
    
    def rayCast(s, loc1, loc2): # all the locs along the line between the center of two locs
        # moving three x pixels at a time
        x1, y1 = s.getCenterCoords(loc1)
        x2, y2 = s.getCenterCoords(loc2)
        rise = y2-y1 ; run = x2-x1
        xStep = int(copysign(3, x2 - x1)) if x2 != x1 else 0
        if xStep:
            yStep = xStep * rise / run
            rangee = range(0, run, xStep)
        else:
            yStep =  int(copysign(s.SS, y2 - y1)) # should be able to take big jumps if x isn't changing
            rangee = range(0, rise, yStep)  
        result = set()
        for _ in rangee:
            x1 += xStep ; y1 += yStep
            result.add(s.getLoc(x1,y1))
        return result
    
    def aStar(s, start, end, obstacle = lambda val: bool(val)):
        def h(loc):
            return abs(end[0]-loc[0]) + abs(end[1]-loc[1])
        
        options = {start:(0,h(start))} # loc: (g(loc), h(loc))
        cameFroms = {start:None}
        doneLookingAt = []
        while options:
            loc = min(options, key = lambda key: sum(options[key]))
            if loc == end:
                path = [loc]
                cameFrom = cameFroms[loc]
                while cameFrom != None:
                    path.append(cameFrom)
                    cameFrom = cameFroms[cameFrom]
                return path

            for neighbor in s.getCardinalNeighbors(loc):
                if not obstacle(s[neighbor]) and not neighbor in doneLookingAt:
                    if neighbor in options:
                        if options[loc][1]+1 < options[neighbor][1]: # if g(loc) improved
                            options[neighbor][1] = options[loc][1]+1
                            cameFroms[neighbor] = loc
                    else:
                        options[neighbor] = (h(neighbor), options[loc][1]+1)
                        cameFroms[neighbor] = loc
            del options[loc] # have to do at end because need g info from
            doneLookingAt.append(loc)
        return False


import pygame as pg

class PgGrid(Grid):
    def __init__(s, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def getRect(s, loc):
        coli, rowi = loc
        return  pg.Rect(coli*s.SS+s.offsetX, rowi*s.SS+s.offsetY, s.SS,s.SS)
    def getAllRects(s):
        return [s.getRect(loc) for loc in s]
    def renderAllLocs(s, win, colorFunc = None):
        if not colorFunc:
            colorFunc = lambda loc: 'black' if bool(s[loc]) else 'white'
        for coli in range(s.nCols):
            for rowi in range(s.nRows):
                pg.draw.rect(win, colorFunc((coli,rowi)), s.getRect((coli,rowi)))
    def renderLoc(s, win, loc, color):
        pg.draw.rect(win, color, s.getRect(loc))

    # could probably add more features but it works. like rn i think it turns it into a square but if something wanted to stay rectangular can just center one of the axises
    # any jpg or png for sure
    def blit(s, win, surface, loc):
        scaled = pg.transform.scale(surface, (s.SS,s.SS))
        win.blit(scaled, s.getCornerCoords(loc))


# imported like this as not to override the name Grid
import tkinter as tk
class TkGrid(Grid):
    def __init__(s, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def renderAllLocs(s, canvas, colorFunc = None):
        if not colorFunc:
            colorFunc = lambda loc: 'black' if bool(s[loc]) else 'white'
        for coli in range(s.nCols):
            for rowi in range(s.nRows):
                x, y = s.getCornerCoords((coli,rowi))
                canvas.create_rectangle(x,y,x+s.SS, y+s.SS, fill=colorFunc((coli,rowi)), width=0)
                print(colorFunc((coli,rowi)))
    def renderLoc(s, canvas, loc, color):
        x, y = s.getCornerCoords(loc)
        canvas.create_rectangle(x,y,x+s.SS, y+s.SS, fill=color, width=0)



if __name__=='__main__':
    grid = TkGrid(5, 4)
    grid.setLocs([(1,0),(4,1),(2,2),(1,3),(4,3)], True)
    root = tk.Tk()
    dims = grid.getWinDimensions()
    c = tk.Canvas(root, width=dims[0], height=dims[1])
    c.pack()
    grid.renderAllLocs(c)
    input()


    '''g = PgGrid(5,4)
    g.setLocs([(1,0),(4,1),(2,2),(1,3),(4,3)], True)
    pg.init()
    win = pg.display.set_mode(g.getWinDimensions())
    g.renderAllLocs(win)
    g.renderLoc(win, (0,0), 'red')
    img = pg.image.load("kids.jpg").convert_alpha()

    g.blit(win, img, (1,1))
    pg.display.flip()
    input()'''


    #g.display(charFunc = lambda val: '*' if val else ' ', border=True)

