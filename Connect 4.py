from copy import deepcopy
from itertools import chain
from math import inf
from random import choice

W = 7 ; H = 6
b = [[None for i in range(H)] for i2 in range(W)] # list of columns
max_depth = 4


def print_board():
    for row_i in range(H-1,-1,-1):
        to_print = [b[col_i][row_i] for col_i in range(W)]
        for i,cell in enumerate(to_print):
            if not cell:
                to_print[i]= ' '
        print(*to_print)
    print('-'*(2*W-1))
    print(*list(range(W)))

def count_blockages(b,col,row,symbol):
    blocking_symbol = 'O' if symbol=='X' else 'X'
    blockages = 0
    try:
        if b[col][row] == blocking_symbol:
            blockages += 1
    except:
        blockages += 1
            
    return blockages
    
    
def count_streaks(b, length, symbol, check_blockage=False):
    streaks = 0
    blockages = 0

    # look in rows
    for row_i in range(H):
        for col_start_i in range(W-length+1): #+1 bc 2nd param not counted
            cells = [b[col_start_i+j][row_i] for j in range(length)]
            if all(cell==symbol for cell in cells):
                streaks += 1
                blockages += count_blockages(b, col_start_i-1,row_i, symbol)
                blockages += count_blockages(b, col_start_i+length,row_i, symbol)
            
    # look in columns 
    for col_i in range(W):
        for row_start_i in range(H-length+1):
            cells = [b[col_i][row_start_i+j] for j in range(length)]
            if all(cell==symbol for cell in cells):
                streaks += 1
                blockages += count_blockages(b, col_i,row_start_i-1, symbol)
                blockages += count_blockages(b, col_i,row_start_i+length, symbol)

    # look for diagnals w/ pos slope
    for col_i in range(W-length+1):
        for row_i in range(H-length+1):
            cells = [b[col_i+i][row_i+i] for i in range(length)]
            if all(cell==symbol for cell in cells):
                streaks += 1
                blockages += count_blockages(b, col_i-1, row_i-1, symbol)
                blockages += count_blockages(b, col_i+length, row_i+length, symbol)

    # look for diagnals w/ neg slope
    for col_i in range(W-length+1):
        for row_i in range(length-1,H):
            cells = [b[col_i+i][row_i-i] for i in range(length)]
            if all(cell==symbol for cell in cells):
                streaks += 1
                blockages += count_blockages(b, col_i-1, row_i+length, symbol)
                blockages += count_blockages(b, col_i+length, row_i-1, symbol)
                
    
    # idk if this is valid math but each blockage stops half the streak from expanding
    return streaks - (blockages/2 if check_blockage else 0)


class Player:
    def minimax(s,b, depth=0, maximizing=False):

        if depth == max_depth:
            return s.eval_b(b, at_max_depth=True)

        evaluation = s.eval_b(b)
        if abs(evaluation) == inf or depth == max_depth:
            return evaluation

        if maximizing:
            best_score = -inf
            for col_i,column in enumerate(b):
                if not None in column:
                    continue
                row_i = column.index(None)
                b[col_i][row_i] = comp_symbol
                score = s.minimax(b,depth+1,False)
                b[col_i][row_i] = None
                best_score = max(best_score,score)

            return best_score

        if not maximizing:
            worst_score = inf
            for col_i,column in enumerate(b):
                if not None in column:
                    continue
                row_i = column.index(None)
                b[col_i][row_i] = user_symbol
                score = s.minimax(b,depth+1,True)
                b[col_i][row_i] = None
                worst_score = min(worst_score,score)
                
            return worst_score
                 
        

    def eval_b(s,b, at_max_depth=False):
        if count_streaks(b,4,comp_symbol):
            return inf
        if count_streaks(b,4,user_symbol):
            return -inf

        if at_max_depth:
            if max_depth%2 == 0:
                return 1*count_streaks(b,3,comp_symbol, check_blockage=True) - 10*count_streaks(b,3,user_symbol, check_blockage=True)
            else:
                return 10*count_streaks(b,3,comp_symbol, check_blockage=True) - 1*count_streaks(b,3,user_symbol, check_blockage=True)
        else:
            return 5*count_streaks(b,3,comp_symbol, check_blockage=True) - 4*count_streaks(b,3,user_symbol, check_blockage=True)




comp_symbol = choice(['X','O'])
user_symbol = 'O' if comp_symbol=='X' else 'X'
if comp_symbol == 'X':
    print('\nThe computer is going first as X.\n')
    turn = 'comp'
else:
    print('\nYou are going first as X\n')
    turn = 'user'



p = Player()
print_board()


while None in list(chain(*b)) and not count_streaks(b,4,user_symbol) and not count_streaks(b,4,comp_symbol):
    # computer's turn
    if turn == 'comp':
        best_score = -inf
        for col_i,column in enumerate(b):
            if not None in column:
                continue
            
            # make move and undo it later
            row_i = column.index(None)
            b[col_i][row_i] = comp_symbol
            score = p.minimax(b)
            b[col_i][row_i] = None
            if score > best_score:
                best_score = score
                best_col_i = col_i

        # place the piece
        b[best_col_i][b[best_col_i].index(None)] = comp_symbol
            

    # user's turn
    elif turn == 'user':
        col_i = -1 # start with something invalid
        while not (col_i in range(W) and None in b[col_i]):

            col_i = input(f'Column (0-{W-1}):  ')
            if col_i.isdigit():
                col_i = int(col_i)
            else:
                continue

        # place the piece
        b[col_i][b[col_i].index(None)] = user_symbol
    

    # after turn
    print('\n'*9)
    print_board()
    turn = 'user' if turn == 'comp' else 'comp'

if count_streaks(b,4,user_symbol):
    print('User wins')
elif count_streaks(b,4,comp_symbol):
    print('Computer wins')
else:
    print('Tie')
