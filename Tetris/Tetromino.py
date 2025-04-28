class Tetromino:
    def __init__(s, name):
        s.name = name
        if name == 'i':
            s.locs = [(5, 0), (5, 1), (5, 2), (5, 3)]
            s.color = '#0DFF72'
            s.ref = [4.5,1.5]
            s.num_orientations = 2
        elif name == 'j':
            s.locs = [(4, 0), (4, 1), (3, 2), (4, 2)]
            s.color = '#FF8E0C'
            s.ref = [4.5, 1.5]
            s.num_orientations = 4
        elif name == 'l':
            s.locs = [(4, 0), (4, 1), (4, 2), (5, 2)]
            s.color = '#F438FF'
            s.ref = [4.5, 1.5]
            s.num_orientations = 4
        elif name == 'o':
            s.locs = [(4, 0), (5, 0), (4, 1), (5, 1)]
            s.color = '#0EC2FF'
            s.ref = [4.5,0.5]
            s.num_orientations = 1
        elif name == 'z':
            s.locs = [(4, 1), (4, 2), (5, 0), (5, 1)]
            s.color = '#3878FF'
            s.ref = [4.5,.5]
            s.num_orientations = 2
        elif name == 't':
            s.locs = [(4, 0), (4, 1), (4, 2), (5, 1)]
            s.color = '#FF0D73'
            s.ref = [4.5,1.5]
            s.num_orientations = 4
        elif name == 's':
            s.locs = [(4, 0), (4, 1), (5, 1), (5, 2)]
            s.color = '#FFE138'
            s.ref = [4.5, .5]
            s.num_orientations = 2

    def left(s):
        s.locs =  [(loc[0]-1,loc[1]) for loc in s.locs]
        s.ref[0] -= 1
    
    def right(s):
        s.locs =  [(loc[0]+1,loc[1]) for loc in s.locs]
        s.ref[0] += 1

    def down(s):
        s.locs =  [(loc[0],loc[1]+1) for loc in s.locs]
        s.ref[1] += 1

    def turn(s):
        s.locs = [(int(s.ref[0]+s.ref[1]-loc[1]), int(loc[0]+s.ref[1]-s.ref[0])) for loc in s.locs]