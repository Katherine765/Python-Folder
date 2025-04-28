ranking={'e':1233,'a':979,'r':899,'o':754,'t':719,'l':719,'i':671,'s':669,'n':575,'c':477,'u':467,'y':425,'d':393, 'h':389,'p':367,'m':316,'g':311,'b':281,'f':230,'k':210,'w':195,'v':153,'z':40,'x':37,'q':29,'j':27}
placement={0: [141, 304, 307, 163, 64], 1: [173, 16, 57, 24, 11], 2: [198, 40, 56, 152, 31], 3: [111, 20, 75, 69, 118], 4: [72, 242, 177, 318, 424], 5: [136, 8, 25, 35, 26], 6: [115, 12, 67, 76, 41], 7: [69, 144, 9, 28, 139], 8: [34, 202, 266, 158, 11], 9: [20, 2, 3, 2, 0], 10: [20, 10, 12, 55, 113], 11: [88, 201, 112, 162, 156], 12: [107, 38, 61, 68, 42], 13: [37, 87, 139, 182, 130], 14: [41, 279, 244, 132, 58], 15: [142, 61, 58, 50, 56], 16: [23, 5, 1, 0, 0], 17: [105, 267, 163, 152, 212], 18: [366, 16, 80, 171, 36], 19: [149, 77, 111, 139, 253], 20: [33, 186, 165, 82, 1], 21: [43, 15, 49, 46, 0], 22: [83, 44, 26, 25, 17], 23: [0, 14, 12, 3, 8], 24: [6, 23, 29, 3, 364], 25: [3, 2, 11, 20, 4]}

import random
import time

#Create wordlist
wordlist = []
with open('wordle_words1.txt', 'r') as file:
    wordlist=[line.strip() for line in file.readlines()]

def entireProgram(wordlist, word, ranking, placement):
    if not word in wordlist:
        print('Word not in wordlist.')
        return False

    #Set variables and lists
    wrong, not_the_word, somewhere=[], [], []
    know=[None,None,None,None,None]
    check=None
    yellow={0:[],1:[],2:[],3:[],4:[]}
    tries=0


    while True:

        #Goes through potential guesses until one is valid
        topRank=0
        topChoice=None
        for potential_guess in wordlist:
            check=True
            guess_list=list(potential_guess)

            #grey and yellow
            for x, letter in enumerate(guess_list):
                if letter in wrong or letter in yellow[x]:
                    check=False

            #Check to make sure somewhere letters are in the word
            if check:
                for x, letter in enumerate(somewhere):
                    if not letter in guess_list:
                        check=False

            #Check to make sure right letters are in the right place
            if check:
                for x, letter in enumerate(know):
                    if not letter==None and not letter==guess_list[x]:
                        check=False
                 
            #Which possible word is best
            if check:
                rank=0
                for x, letter in enumerate(guess_list):
                    #only the first occurance counts
                    if x == potential_guess.find(letter):
                        rank += ranking[letter]
                    #can get placement points for multiple occurences
                    #change dec for weighing it
                    rank=rank+.55*(placement[ord(letter)-97])[x]

                if rank > topRank:
                    topRank=rank
                    topChoice=potential_guess
 
        print(topChoice)
        guess_list=list(topChoice)
        tries += 1

        #Actual check
        #Word correct
        if word==topChoice:
            print('\nWin in %s tries!' %tries)
            return tries
        #check each letter
        for x, letter in enumerate(guess_list):
            #Green 
            if letter == word[x]:
                know[x]=letter
            #Yellow
            elif letter in word:
                somewhere.append(letter)
                yellow[x].append(letter)
            #Grey
            else: #not letter in word and not letter in wrong:
                wrong.append(letter)

word = random.choice(wordlist)
entireProgram(wordlist,word,ranking,placement)