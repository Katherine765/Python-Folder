from copy import deepcopy as dc
from math import inf
wins = ['012', '345', '678', '036', '147', '258', '048', '246']

class TTT():
    def __init__(s):
        s.spaces = ['.' for _ in range(9)]
    
    def drawBoard(s):
        print()
        for x in range(0, 9, 3):
            print(f'{s.spaces[x]}{s.spaces[x+1]}{s.spaces[x+2]}  {x+1}{x+2}{x+3}')

    def place(s, space, sym, fromUser=False):
        if type(space)==str and not space.isdigit():
            return False
        space = int(space)
        if fromUser:
            space -= 1
        if not space in range(10):
            return False
        if not s.spaces[space] == '.':
            return False
        s.spaces[space] = sym
        return True

    def checkBoard(s):
        for win in wins:
            winList = [int(x) for x in win]
            if s.spaces[winList[0]] == s.spaces[winList[1]] == s.spaces[winList[2]] != '.':
                return s.spaces[winList[0]]

        if not '.' in s.spaces:
            return 'tie'

        return False


class AI:
    @staticmethod
    def move(game):
        best_score = -inf
        for space in range(9):
            simulation = dc(game)
            if not simulation.place(space,'O'):
                continue

            score = AI.minimax(simulation)
            if score > best_score:
                best_score = score
                best_space = space
        
        game.place(best_space,'O')
    
    @staticmethod
    def minimax(game, role='minimizing'):
        result = game.checkBoard()
        if result:
            return {'X':-1, 'O':1, 'tie':0}[result]

        if role=='maximizing':
            best_score = -inf
            for space in range(9):
                simulation = dc(game)
                if not simulation.place(space, 'O'):
                    continue
                score = AI.minimax(simulation, role='minimizing')
                best_score = max(score,best_score)
            return best_score

        if role=='minimizing':
            worst_score = inf
            for space in range(9):
                simulation = dc(game)
                if not simulation.place(space, 'X'):
                    continue
                score = AI.minimax(simulation, role='maximizing')
                worst_score = min(score,worst_score)
            return worst_score


class User:
    @staticmethod
    def move(game):
        space = input(f'Space:   ')
        if not game.place(space, 'X', fromUser=True):
            User.move(game)

        

game = TTT()
while True:
    for cls in (User, AI):
        game.drawBoard()
        cls.move(game)
        if game.checkBoard():
            game.drawBoard()
            quit()
