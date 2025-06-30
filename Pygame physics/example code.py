    '''Cell = getCellCreator([],{'filled':False})
    def valueFunc(loc):
        return Cell(filled=loc[1] == 7 or loc==(5,6))
    grid = PgGrid(10,10,valueFunc=valueFunc)
    win =  pg.display.set_mode((500,500))
    def colorFunc(loc):
        return 'dark gray' if grid[loc]['filled'] else 'white'
    grid.render(win, colorFunc=colorFunc)
    pg.display.update()'''
