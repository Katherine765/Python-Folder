import random
import time

#Open wordlists and select word
wordlist = []
with open('wordle_words1.txt', 'r') as file:
    wordlist=[line.strip() for line in file.readlines()]
        
word = random.choice(wordlist)

guessable_words=[]
with open('wordle_words2.txt', 'r') as file2:
    for line in file2.readlines():
        guessable_words.append(line.strip())

#Shuffle wordlist for cheater
random.shuffle(wordlist)

remaining=6
guess_number, letter_number=0,0
#Cheating related:
wrong, somewhere=[],[]
know=[None,None,None,None,None]
check=None
yellow={0:[],1:[],2:[],3:[],4:[]}
tries=0

from tkinter import *
Wordle=Tk()
canvas=Canvas(Wordle, width=400, height=500)
canvas.pack()

entry=Entry()
entry.pack()

#--------SETUP COMPLETE------------------------------------------------------------------------------------------------------------------------------------

#Draw letter function definition
def draw_letter(character,color,word_number,character_number):
    canvas.create_text(45*letter_number+110 ,65*word_number, text=character, font=('Courier 50 bold'), fill=color)

#won't run after the player has made guesses sometimes
def cheat():
    #Goes through potential guesses until one is valid
    for potential_guess in wordlist:
        check=True
        guess_list=list(potential_guess)
        
        #Check for grey letters
        for letter in guess_list:
             if letter in wrong:
                 check=False
        #Check that all yellow letters are in word
        if check:
            for x, letter in enumerate(somewhere):
                if not letter in guess_list:
                    check=False
        #Check that all green letters are where they should be
        if check:
            for x in range(0,5):
                if not know[x] == None and not guess_list[x] == know[x]:
                    check=False
        #Check that yellow letters aren't where they were before
        if check:
            for x, letter in enumerate(guess_list):
                if letter in yellow[x]:
                    check=False

        #Check that the guess isn't actually the word
        if check:
            if potential_guess==word:  
                print('avoided word')
                check=False
                global guess
                guess= potential_guess

        #Checking complete - enter word
        if check:
            guess=potential_guess
            break
        elif guess == word and wordlist[2314]==potential_guess:
            from tkinter import messagebox
            response= messagebox.askokcancel(message = 'There is only one possible answer remaining. Would you still like help?')
            if response == False:
                guess = 'none'

#What happens once guess is submitted:
def click(event=0):
    
    #Record guess and clear entry box
    global guess
    guess=entry.get()
    entry.delete(0, END)
    
    if guess == 'help':
        cheat()
    
    #Checks if word is valid
    if guess in wordlist or guess in guessable_words:
        
        global guess_number, remaining, letter_number
        guess_number += 1
        remaining += -1
        letter_number=0

        #Actual check
        for x, letter in enumerate(guess):
            if letter in word:
                if letter == word[letter_number]:
                    global know
                    know[letter_number]=letter
                    draw_letter(letter, 'forest green',guess_number, letter_number)
                else:
                    global somewhere, yellow
                    somewhere.append(letter)
                    yellow[x].append(letter)
                    draw_letter(letter, 'goldenrod1', guess_number, letter_number)
            else:
                global wrong
                wrong.append(letter)
                draw_letter(letter, 'gray60', guess_number, letter_number)

            letter_number += 1
            Wordle.update()
            time.sleep(.3)

    #Checks if user won or lost; if so removes ability to submit new answers       
    if guess == word:
        entry.destroy(); button.destroy()
        canvas.create_text(200, 480, text='You won in %s guesses!' %(guess_number), font=35)
    if remaining==0 and not guess==word:
        entry.destroy(); button.destroy()
        canvas.create_text(200, 450, text='You ran out of guesses.', font=35)
        canvas.create_text(200, 480, text='The word was %s.' %(word), font=35)

#Enter can be pressed to submit andwer and run click sequence. Pressing the button also submits.
canvas.bind_all('<KeyPress-Return>', click)
button=Button(text='Submit', command=click)
button.pack()

mainloop()