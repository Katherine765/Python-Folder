from itertools import groupby
from copy import copy

class StreakGetter:
    # appears to be working
    def __init__(s, W, H):
        def find_diag(start_coli, start_rowi, coli_inc, rowi_inc):
            diag = []
            coli = copy(start_coli) ; rowi = copy(start_rowi)
            while coli in range(W) and rowi in range(H):
                diag.append((coli,rowi))
                coli += coli_inc
                rowi += rowi_inc
            return diag

        s.lines_locs = []
        s.lines_locs.extend([[(coli,rowi) for coli in range(W)] for rowi in range(H)])
        s.lines_locs.extend([[(coli,rowi) for rowi in range(H)] for coli in range(W)])

        # mostly neg-sloped diags (bc starts in top left)
        for start_coli in range(W):
            s.lines_locs.append(find_diag(start_coli, 0, 1,1))
            s.lines_locs.append(find_diag(start_coli, H-1, 1,-1)) # pos-sloped
        for start_rowi in range(1,H):
            s.lines_locs.append(find_diag(0, start_rowi, 1,1))
        # rest of pos-sloped diags
        for start_rowi in range(H-1):
            s.lines_locs.append(find_diag(0, start_rowi, 1,-1))

    def main(s, syms, length, b):
        result = 0
        keyfunc = lambda x: 'target' if x in syms else 'ignore'
        for line_locs in s.lines_locs:
            line = [b[loc] for loc in line_locs]
            for key, group in groupby(line, key=keyfunc):
                glen = len(list(group))
                if key =='target' and glen >= length:
                    result += glen-length+1
        return result
