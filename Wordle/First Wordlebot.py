wordlist = []
with open('wordle_words1.txt', 'r') as file:
    wordlist=[line.strip() for line in file.readlines()]

import random
#random.shuffle(wordlist)

def find_guess():
    #Goes through potential guesses until one is valid
    for word in wordlist:
        check = True
        guess_list=list(word)

        #no wrong letters
        for i, letter in enumerate(word):
            if letter in wrong or letter in yellow[i]:
                 check = False
                 break

        #somewhere letters in word
        if check:
            for x, letter in enumerate(somewhere):
                if not letter in guess_list:
                    check = False
                    break

        #green letters in right place
        if check:
            for x, letter in enumerate(know):
                if not letter is None and not letter==guess_list[x]:
                    check = False
                    break

        if check:
            return word


for word in wordlist:
    wrong, somewhere, = [], []
    know=[None for x in range(5)]
    yellow={x:[] for x in range(5)}
    tries=0
    total_tries = 0
    run = True
    while run:
        guess = find_guess()
        print(guess)
        tries += 1


        if word==guess:
            print('\nWin in %s tries!' %tries)
            total_tries += 0
            run = False

        if run:
            #Actual check
            for x, letter in enumerate(guess):
                #Green  
                if letter == word[x]:
                    know[x]=letter
                #Yellow
                elif letter in word and not letter in somewhere:
                    somewhere.append(letter)
                    yellow[x].append(letter)
                #Grey
                if not letter in word and not letter in wrong:
                    wrong.append(letter)

#got stuck once
print(total_tries/len(wordlist))
