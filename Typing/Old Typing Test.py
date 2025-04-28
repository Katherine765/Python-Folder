import random
import time
from tkinter import *
class Test():
    def __init__(self, canvas, wordCount):
        self.wordCount=wordCount
        self.wordList=[]
        self.typedCount= 0
        self.test=None
        self.wrong=0
        self.timer=0
        self.results=None
        self.check=None
        self.lines=1
        self.used=1
        self.spaces=[]
        self.place=0
        self.canvas=canvas
        self.canvas.bind_all('<KeyPress>', self.changeColor)
        
    def create(self):
        #Make wordlist
        file=open('words.txt', 'r')
        self.wordList=[]
        for line in file.readlines():
            self.wordList.append(line.strip())

        #Create test from wordlist in var form
        self.wordlList=random.shuffle(self.wordList)
        testList=self.wordList[0:self.wordCount]
        self.test=' '.join(testList)
    
    def draw(self):
        
        #basically copied this code from a website, finds where the spaces are
        while self.test.find(' ', self.place) != -1:
            self.spaces.append(self.test.find(' ', self.place))
            self.place=self.test.find(' ', self.place) + 2
 
        for x in range(0, len(self.test)):
            self.canvas.create_text(18*self.used+18, 35*self.lines, text=self.test[x], font='Courier 18')            
            self.used=self.used+1

            if x in self.spaces:
                #ok so... the first part of the subtraction is the index of the next space
                #subtracting the current index get how many characters are between them
                #adding that to how many characters are already in and seeing if that will fit is when this is run
                #idk why the +1 needs to be there
                if self.spaces.index(x)+1 == len(self.spaces):
                    if self.used +(len(self.test)-x) > 65:
                        self.lines = self.lines+1
                        self.used=0
                elif self.used +(self.spaces[self.spaces.index(x)+1]-x) > 65:
                    self.lines = self.lines+1
                    self.used=0

    def changeColor(self, event):
        #first time
        if self.timer == 0:
            self.timer = time.time()

        #Changecolor part
        if event.char==self.test[self.typedCount]:
            self.typedCount=self.typedCount+1
            self.canvas.itemconfig(self.typedCount, fill='green')
        else:
            self.canvas.itemconfig(self.typedCount+1, fill='red')
            # same character won't be counted as wrong more than once
            if not self.check == self.typedCount:
                self.check=self.typedCount
                self.wrong=self.wrong+1

        if self.typedCount==len(self.test):
            self.endGame()
            
    def endGame(self):
        self.timer=time.time()-self.timer
        WPM=round(self.typedCount/5/(self.timer/60), 2)
        self.results='WPM: ' + str(WPM) + ('    Acc: ' + str(round((len(self.test)-self.wrong)/len(self.test)*100,2)))
        self.canvas.create_text(600, 425, text=self.results, font='Courier 25')


tk=Tk()
global canvas
canvas=Canvas(tk, width=1200, height=450)
canvas.pack()
tk.update()

global entry
entry=Entry()
entry.pack()

def enter():
    global entry
    count=entry.get()
    entry.destroy()
    global button
    button.destroy()
    global canvas
    test=Test(canvas, int(count))
    test.create()
    test.draw()           
global button  
button=Button(text='Submit Wordcount', command=enter)
count=button.config(command=enter)
button.pack()

#if it isn't openned w/ idle
mainloop()
