from random import shuffle
import time
from tkinter import *
from tkinter import font

WORDLIST_LENGTH = 500

with open('words_by_freq.txt', 'r') as file:
    wordlist=[line.strip() for line in file.readlines()]
    wordlist = wordlist[:WORDLIST_LENGTH]
    shuffle(wordlist)

W = 750 ; PAD = 25 ; NUM_WORDS = 15 ; FONT_SIZE = 25 ; FONT = (f'Cascadia Mono', FONT_SIZE) #can add "Semibold"
FONT_WIDTH = FONT_SIZE * .8 ; FONT_HEIGHT = FONT_SIZE



class Game():
    def __init__(s):
        s.index = 0 # how many chars have been typed
        s.start_time = None
        s.already_wrong = False
        s.mistake_count = 0

        s.test_string = '' # all one string
        s.test_list = [''] # to be broken up by line
        s.c_items = []
        for word in wordlist[:NUM_WORDS]:
            word = word + ' '
            s.test_string += word
            if len(s.test_list[-1]) + len(word) <= (W-PAD*2)/FONT_WIDTH:
                s.test_list[-1] += word
            else:
                s.test_list.append(word)

            for i, letter in enumerate(word):
                x = PAD + FONT_WIDTH/2 + FONT_WIDTH*(len(s.test_list[-1]) - len(word) + i)
                y = PAD + FONT_HEIGHT/2 + (len(s.test_list)-1)*(PAD+FONT_HEIGHT)
                s.c_items.append(c.create_text(x,y,text=letter,font = FONT, fill='#636568'))

        s.test_string = s.test_string[:-1] # remove last space
        s.test_list[-1] = s.test_list[-1][:-1]
        del s.c_items[-1] # would this even matter

        s.c_height = PAD*2+(FONT_HEIGHT+PAD)*len(s.test_list) + 75
        c.config(height = s.c_height) # fix height, 50 for score at end

    def keypress(s, e):
        if not s.start_time:
            s.start_time = time.time()

        if e.char == s.test_string[s.index]:
            c.itemconfig(s.c_items[s.index], fill='#D1D0C5')
            s.index += 1
        else:
            c.itemconfig(s.c_items[s.index], fill='#BB4551')
            if not s.already_wrong:
                s.mistake_count += 1

        if s.index==len(s.test_string):
            s.display_results()
            
    def display_results(s):
        total_time = time.time() - s.start_time
        WPM = s.index/5/(total_time/60)

        acc = (s.index-s.mistake_count) / s.index
        c.create_text(W/2, s.c_height-30, text=f'WPM: {WPM:.2f}  Acc: {acc:.2f}', font=FONT, fill='#D1D0C5')
        c.unbind_all('<KeyPress>')


tk=Tk()
c=Canvas(tk, height=20, width=W, bg='#323437') # height is temporary, it will be changed in game initiation
c.pack()

g = Game()
c.bind_all('<KeyPress>', g.keypress)
mainloop()
