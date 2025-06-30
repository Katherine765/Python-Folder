import Grid
import PgPhysEntity
import pygame as pg
import random as r

nCols = 20 ; nRows = 15 ; SS = 50
#W = nCols * SS ; H = nRows * SS

class Game:
    def __init__(s):
        s.tileMap = Grid.PgGrid(nCols,nRows)
        s.tileMap.setLocs(r.sample(list(s.tileMap.keys()), int(nCols*nRows/4)), True)
        s.player = PgPhysEntity.PgPhysEntity(s.tileMap)

    def main(s):
        pg.init()
        win = pg.display.set_mode(s.tileMap.getWinDimensions())
        clock = pg.time.Clock()
        while True:
            dt = clock.tick(60) / 1000
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                arrowDir = -1
            elif keys[pg.K_RIGHT]:
                arrowDir = 1
            else:
                arrowDir = 0

            for e in pg.event.get():
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_UP:
                        s.player.jump()
                if e.type == pg.QUIT:
                    pg.quit()
                    quit()

            win.fill('black')
            s.tileMap.renderAllLocs(win)
            s.player.update(dt, arrowDir)
            s.player.render(win)
            pg.display.flip()

Game().main()