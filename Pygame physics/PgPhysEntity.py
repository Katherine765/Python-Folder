import pygame as pg
import PhysEntity

# implementing out of bounds here makes more sense because there is a tilemap and a plyaer width and heigth
class PgPhysEntity(PhysEntity.PhysEntity):
    def __init__(s, tileMap, collideFunc=None):
        super().__init__()
        s.size = (10,10)
        s.tileMap = tileMap
        s.w, s.h = s.tileMap.getWinDimensions()
        if not collideFunc:
            s.collideFunc = lambda loc: bool(s.tileMap[loc])

    def update(s, dt, arrowDir):
        # this is mostly just collision stuff with a tilemap
        movement = s.updateX(dt, arrowDir)
        rect = s.rect()
        if rect.left < 0:
            rect.left = 0
            s.vel[0] = 0
        if rect.right > s.w - s.size[0]:
            rect.right = s.w
            s.vel[0] = 0
        for loc in s.tileMap:
            if not s.collideFunc(loc):
                continue
            rect2 = s.tileMap.getRect(loc)
            if rect.colliderect(rect2):
                if movement > 0:
                    rect.right = rect2.left
                if movement < 0:
                    rect.left = rect2.right
        s.pos[0] = rect.x

        movement = s.updateY(dt)
        rect = s.rect()
        if rect.top < 0:
            rect.top = 0
            s.vel[1] = 0
        if rect.bottom > s.h - s.size[1]:
            rect.bottom = s.h 
            s.vel[1] = 0
        for loc in s.tileMap:
            if not s.collideFunc(loc):
                continue
            rect2 = s.tileMap.getRect(loc)
            if rect.colliderect(rect2):
                if movement > 0:
                    rect.bottom = rect2.top
                    s.vel[1] = 0
                    s.jumps = 0
                if movement < 0:
                    rect.top = rect2.bottom
                    s.vel[1] = 0
        s.pos[1] = rect.y


    def rect(s):
        return pg.Rect(*s.pos, *s.size)
    
    def render(s, win, color='black'):
        pg.draw.rect(win, color, s.rect())

    

