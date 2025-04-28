import random
import time
from tkinter import *

class Pipe():
    def __init__(self, canvas, bird, start=1000):
        self.canvas=canvas
        self.start=start
        self.pos=self.start
        gap=random.randint(10, 440)
        #topleft x, topleft y, bottomright x, bottomleft y
        #pretty cool - figured out that you can put the two parts in a list
        self.ident=[canvas.create_rectangle(self.start, 0, self.start+30, gap, fill='aquamarine3'),\
                 canvas.create_rectangle(self.start, gap+150, self.start+30, 605, fill='aquamarine3')]




    def delete(self):
        canvas.delete(self)
    
class Bird():
    def __init__(self, canvas, direction='down', ups=0, pos=300):
        self.canvas=canvas
        self.canvas.bind_all('<KeyRelease>', self.switch)
        self.ident=canvas.create_rectangle(20, 300, 50, 330, fill='gold1')
        self.direction=direction
        self.ups=ups
        self.pos=pos
    def switch(self, event):
        self.direction='up'
        self.fly()
    def fly(self):
        if self.direction == 'up':  
            #to make it less choppy, have to have time.sleep in between, which is in the main loop
            if self.ups < 5:
                self.canvas.move(self.ident, 0, -11)
                self.ups=self.ups+1
                self.pos = self.pos-11
            elif self.ups > 7:
                self.direction = 'down'
                self.ups=0
            else:
                #pauses between up and down
                self.ups=self.ups+1
        else:
            self.canvas.move(self.ident, 0, +3)
            self.pos = self.pos +3     

tk=Tk()
canvas=Canvas(tk, width=1000, height=600)
canvas.pack()
tk.update()
bird=Bird(canvas)


pipes=[]
score=0
#numbers are weird bc canvas goes from -20 to 1000. now switching to 3 pipes
#numbers for 4 pipes: 227.5, 495, 752.5, 1000
pipes.append(Pipe(canvas, bird, start=320))
pipes.append(Pipe(canvas, bird, start=660))
pipes.append(Pipe(canvas, bird))

def mover(pipeNum):
    #pipes is a list, ident is a list bc a pipe has two parts
    pipes[pipeNum].canvas.move(pipes[pipeNum].ident[0], -3, 0)
    pipes[pipeNum].canvas.move(pipes[pipeNum].ident[1], -3, 0)
    pipes[pipeNum].pos = pipes[pipeNum].pos - 3



#While bird isn't touching any pipes (change if wigets are added or if bird start pos changes)
while len(canvas.find_overlapping(20, bird.pos, 50, bird.pos+30)) == 1:
    mover(0)
    mover(1)
    mover(2)
    #mover(3)
    bird.fly()
    tk.update()

    #changed to change number of pipes
    for x in range (0,3):
        if pipes[x].pos <= -30:
            pipes.append(Pipe(canvas, bird))
            #deletes the rectangle - omg this took forever to figure out
            canvas.delete(pipes[x].ident[0])
            canvas.delete(pipes[x].ident[1])
            #deletes the item from the list
            del pipes[x]
            tk.update()
            score=score+1
    time.sleep(.0005)

print('Score %s' %score)
#canvas.delete('all')