with open('Words_2.txt', 'r') as file:
    wordlist= [line for line in file.readlines()]

import random
word = random.choice(wordlist).strip().upper()
board = ['_']*len(word)


hangman = ["   \n   \n   ", " 0 \n   \n   ",
           " 0 \n/  \n   ", " 0 \n/| \n   ",
           " 0 \n/|\\\n   ", " 0 \n/|\\\n/  ",
           " 0 \n/|\\\n/ \\"]


def print_board():
    print()
    print(hangman[wrong])
    print(*board)

wrong = 0
already_guessed = []
while '_' in board:
    print_board()
    
    guess = input('Guess:  ').upper()[0]
    if guess in already_guessed:
        already_guessed.append(guess)
    else:
        if guess in word:
            for i, ch in enumerate(word):
                if guess == ch:
                    board[i] = ch
        else:
            wrong += 1
            if wrong == 6:
                break

print_board()
