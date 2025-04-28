#Open wordlists and select word
file=open('wordle_words1.txt', 'r')
wordlist = []
for line in file.readlines():
    wordlist.append(line)
import random
word = str.rstrip(random.choice(wordlist))
word = 'excel'

file=open('wordle_words2.txt','r')
guessable_words = []
for line in file.readlines():
    guessable_words.append(line)

#Define variables
remaining=6
guess_number=0
letter_number=0

#Set up tkinter, canvas, and entry box
from tkinter import *
tk=Tk()
canvas=Canvas(tk, width=400, height=500)
canvas.pack()
entry=Entry()
entry.pack()

import time

#Draw letter function definition
def draw_letter(character,color,word_number,character_number):
    canvas.create_text(45*letter_number+110 ,65*word_number, text=character, font=('Courier 50 bold'), fill=color)

#What happens once guess is submitted:
def click(event=0):
    
    #Record guess and clear entry box
    guess=entry.get()
    entry.delete(0, END)

    #Checks if word is valid
    if guess+'\n' in wordlist or guess+'\n' in guessable_words:

        #Get variables ready         
        global guess_number
        guess_number= guess_number+1
        global remaining
        remaining=remaining-1
        global letter_number
        letter_number=0

        #Letter checking loop
        for letter in guess:
            if letter in word:
                if letter == word[letter_number]:        
                    draw_letter(letter, 'forest green',guess_number, letter_number)
                    tk.update()
                    time.sleep(.3)
                else:
                    draw_letter(letter, 'goldenrod1', guess_number, letter_number)
                    tk.update()
                    time.sleep(.3)
            else:
                draw_letter(letter, 'gray60', guess_number, letter_number)
                tk.update()
                time.sleep(.3)
            letter_number=letter_number+1

    #Checks if user won or lost; if so removes ability to submit new answers       
    if guess == word:
        entry.destroy()
        button.destroy()
        canvas.create_text(200, 480, text='You won in %s guesses!' %(guess_number), font=35)
    if remaining==0 and not guess==word:
        entry.destroy()
        button.destroy()
        canvas.create_text(200, 450, text='Sorry, you ran out of guesses.', font=35)
        canvas.create_text(200, 480, text='The word was %s.' %(word), font=35)

#Enter can be pressed to submit andwer and run click sequence
canvas.bind_all('<KeyPress-Return>', click)

#So can pressing the submit button
button=Button(text='Submit', command=click)
button.pack()
