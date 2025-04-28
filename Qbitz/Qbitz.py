from itertools import chain, cycle
import random as r
import time
from tkinter import *

SS = 90 ; N = 4; COLOR1 = 'white' ; COLOR2 = '#ff3333' ; MEMO_TIME = 5

# could add shortcuts for jumping directly to certain image

class Qbit:
    def __init__(s, x, y, face, exclusion=None):
        s.x = x ; s.y = y
        s.c_items = []

        s.cycler1 = cycle(list(range(5)))
        s.set_face(face)

        s.corners = [[s.x,s.y],[s.x+SS,s.y],[s.x+SS,s.y+SS],[s.x,s.y+SS]]
        s.cycler2 = cycle(s.corners)
        if exclusion:
            s.set_exclusion(exclusion)
        else:
            s.excluded_corner = next(s.cycler2)
        
        s.draw_face()

    def fix_cycler(s, cycler, correct_val):
        actual_val = None
        while actual_val != correct_val:
            actual_val = next(cycler)
        return cycler

    '''def fix_cycler2(s):
        cycler_excluded_corner = None
        while s.excluded_corner != cycler_excluded_corner:
            cycler_excluded_corner = next(s.cycler2)'''
    
    def set_face(s, face):
        s.face = face
        s.cycler1 = s.fix_cycler(s.cycler1, s.face)

    def set_exclusion(s, exclusion):
        s.excluded_corner = s.corners[exclusion]
        s.cycler2 = s.fix_cycler(s.cycler2, s.excluded_corner)


    def draw_face(s):
        c.delete(*s.c_items)
        s.c_items.clear()
        rect_color = COLOR1 if s.face in (0,3) else COLOR2
        s.c_items.append(c.create_rectangle(s.x,s.y,s.x+SS,s.y+SS,fill=rect_color, width=0))
        if s.face in (3, 4):
            PAD = SS/7
            oval_color = COLOR1 if s.face==4 else COLOR2
            s.c_items.append(c.create_oval(s.x+PAD,s.y+PAD,s.x+SS-PAD,s.y+SS-PAD,fill=oval_color, width=0))
        if s.face == 2:
            points = list(chain([corner for corner in s.corners if not corner==s.excluded_corner]))
            s.c_items.append(c.create_polygon(points, fill=COLOR1, width=0))
        
 
    def switch(s):
        s.set_face(next(s.cycler1))
        s.draw_face()

    def rotate(s):
        s.excluded_corner = next(s.cycler2)
        s.draw_face()



class Qbitz:
    def __init__(s):
        s.pattern_faces = {(coli,rowi): r.randint(0,4) for coli in range(N) for rowi in range(N)}
        s.pattern_exclusions = {key:r.randint(0,3) for key, val in s.pattern_faces.items() if val==2}
        s.qbits = {} # no z bc it is literally a list of individual qbits, not the game
        for loc, face in s.pattern_faces.items():
            x = loc[0]*SS ; y = loc[1]*SS
            exclusion = s.pattern_exclusions[loc] if loc in s.pattern_exclusions else None
            s.qbits[loc] = Qbit(x,y,face, exclusion = exclusion)

        tk.update()
        time.sleep(MEMO_TIME)
        s.start_time = time.time()

        for qbit in s.qbits.values():
            qbit.set_face(0)
            qbit.set_exclusion(0)
            qbit.draw_face()
    
    def switch(s,e):
        s.qbits[(e.x//SS,e.y//SS)].switch()

    def rotate(s,e):
        s.qbits[(e.x//SS,e.y//SS)].rotate()

    def end_game(s, e):

        total_time = time.time() - s.start_time
        score = 0
        for loc, correct_face in s.pattern_faces.items():
            qbit = s.qbits[loc]
            if qbit.face == correct_face:
                if not loc in s.pattern_exclusions or qbit.corners[s.pattern_exclusions[loc]] == qbit.excluded_corner:
                    score += 1
        
        c.create_text((N*SS+10)/2, N*SS+30, text=f'Score: {score}    Time:{total_time:.2f}', font = 'Helvetica 20')

    


tk = Tk()
c = Canvas(tk, width=SS*N, height=SS*N+50)
c.pack()

g = Qbitz()
tk.update()

c.bind_all('<s>', g.switch)
c.bind_all('<t>', g.rotate)
c.bind_all('<space>', g.end_game)

tk.mainloop()