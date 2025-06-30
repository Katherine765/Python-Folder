from copy import deepcopy as dc
from math import inf
import StreakGetter

W = 7 ; H = 6
sg = StreakGetter.StreakGetter(W,H).main

class Game:
    def __init__(s):
        s.b = {(coli,rowi):None for rowi in range(H) for coli in range(W)}

    def display(s):
        for rowi in range(H):
            for coli in range(W):
                value = s.b[(coli,rowi)]
                print(value if value else ' ', end=' ')
            print()
        print('-'*(2*W-1))
        print(*list(range(W)))

    def drop(s, coli, sym):
        if type(coli)==str and not coli.isdigit():
            return False
        coli = int(coli)
        if not coli in range(W):
            return False
        for rowi in reversed(range(H)):
            if not s.b[(coli,rowi)]:
                s.b[(coli,rowi)] = sym
                return True
        return False
 
    def check_liveness(s):
        if sg(['X'], 4, s.b) or sg(['O'], 4, s.b):
            return False
        if not None in s.b.values():
            return False
        return True


class AI:
    MAX_DEPTH = 4

    @staticmethod
    def minimax(game, depth=0, role = 'minimizing', alpha=-inf, beta=inf):
        if depth == AI.MAX_DEPTH or not game.check_liveness():
            return AI.evaluate(game)
        
        if role == 'minimizing':
            worst_score = inf 
            for coli in range(W):
                simulation = dc(game)
                if not simulation.drop(coli, 'X'):
                    continue
                score = AI.minimax(simulation,depth+1,'maximizing', alpha, beta)
                worst_score = min(worst_score,score)

                beta = min(beta, score)
                if beta <= alpha:
                    break
            return worst_score
        
        if role == 'maximizing':
            best_score = -inf
            for coli in range(W):
                simulation = dc(game)
                if not simulation.drop(coli, 'O'):
                    continue
                score = AI.minimax(simulation,depth+1,'minimizing', alpha, beta)
                best_score = max(best_score, score)

                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return best_score

    @staticmethod
    def evaluate(game):
        if sg(['O'], 4, game.b):
            return 9999
        if sg(['X'], 4, game.b):
            return -9999 
        # number of potential connect4s
        return sg(['O', None], 4, game.b) - sg(['X', None], 4, game.b)

    
    @staticmethod
    def play(game):
        best_score = -inf

        for coli in range(W):
            simulation = dc(game)
            if not simulation.drop(coli, 'O'):
                continue

            score = AI.minimax(simulation)
            if score > best_score:
                best_score = score
                best_coli = coli

            print(score)
        game.drop(best_coli, 'O')


class User:
    @staticmethod
    def play(game):
        if not game.drop(input(f'Column (0-{W-1}):  '), 'X'):
            User.play(game)


game = Game()
while True:
    for cls in (User,AI):
        game.display()
        cls.play(game)
        if not game.check_liveness():
            game.display()
            quit()