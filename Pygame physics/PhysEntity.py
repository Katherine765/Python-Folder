class PhysEntity:
    def __init__(s):
        # pixels, pixels per sec, sec^2.... in theory but not actuality
        s.pos = [0,0]
        s.vel = [0,0]
        s.acc = [0, 1600]
        s.terminalSpeed = 500
        s.arrowSpeed = 350
        s.jumpVel = -500
        s.jumps = 0
        s.maxJumps = 2

    def updateX(s, dt, arrowDir):
        s.vel[0] = min(s.terminalSpeed, s.vel[0]+s.acc[0]*dt) if s.vel[0]+s.acc[0]*dt>0 else max(-s.terminalSpeed, s.vel[0]+s.acc[0]*dt)
        movement = (arrowDir*s.arrowSpeed + s.vel[0]) * dt
        s.pos[0] += movement
        return movement
    
    def updateY(s, dt):
        s.vel[1] = min(s.terminalSpeed, s.vel[1]+s.acc[1]*dt) if s.vel[1]+s.acc[1]*dt>0 else max(-s.terminalSpeed, s.vel[1]+s.acc[1]*dt)
        movement = s.vel[1] * dt
        s.pos[1] += movement
        return movement
    
    def jump(s):
        if s.jumps < s.maxJumps:
            s.vel[1] = s.jumpVel
            s.jumps += 1
