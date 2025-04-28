from random import randint
while True:
    lowest=int(input('Lowest:  '))
    highest=int(input('Highest:  '))
    number=randint(lowest, highest)
    answer=None
    guesses=0
    while answer != number:
        answer=int(input('\nGuess:  '))
        guesses =+ 1
        if answer != number:
            if answer > number:
                print('Try lower.\n')
            else:
                print('Try higher.\n')
    print(f'\nYou got it right in {guesses} tries!')
    print('Starting Over.\n')