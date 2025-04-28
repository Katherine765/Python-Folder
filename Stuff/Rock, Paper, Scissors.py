from random import choice

# winner: loser
wins={'rock':'scissors','paper':'rock','scissors':'paper'}

#U stands for user, c stands for computer
u_score, c_score=0,0

#How many rounds that the user wants to play
repeat=int(input('# Rounds:  '))

for x in range(repeat):
    c_play=choice(['rock','paper','scissors'])
    
    u_play=input('Play:  ')
    while not u_play in ['rock','paper','scissors']:
        u_play=input('Invalid input. Play:  ')
    
    print(f'Rock, paper, scissors, shoot!  Your play: {u_play}.  Computer play: {c_play}.')

    #Decides who wins the round, then adds score
    if u_play==c_play:
        print('Tie round.')
    elif wins[u_play]==c_play:
        print('You win that round.')
        u_score+=1
    else:
        print('The computer wins that round.')
        c_score+=1

#Shows final winner
if u_score>c_score:
    print(f'\nYou win; the score is {u_score} to {c_score}.')
elif c_score>u_score:
    print(f'\nYou lose; the score is {c_score} to {u_score}.')
else:
    print(f'\nTie with a score of {u_score} to {c_score}!')