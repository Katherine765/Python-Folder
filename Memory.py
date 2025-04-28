#created a version without lists in lists mess, but wasn't worth continuing with bc this already worked

import random
import time

from tkinter import *
tk=Tk()
global canvas
canvas=Canvas(tk, width=700, height=500)
canvas.pack()

global last, score
last=None
score,lines=0,0

#activated inside of line function
def level_complete(circles, clicked, canvas):
    global score
    #If the numbers are in order - very simple solution :)
    if clicked == sorted(clicked):
        #this score stuff isn't working - it is creatign a new variable
        print('Next level')
        score +=1

        #break for 1 second then create the next level
        canvas.delete('all')
        #tk.update() #showing this means that canvas is clear during break
        time.sleep(1)
        create_level(canvas, score)
    else:
        #score printed and numbers shown so user can see what went wrong
        print('Score: %s' %score)
        global text
        for item in text:
            canvas.itemconfigure(item, state='normal')


#activated when user clicks
def line(event):
    global canvas, circles, last, clicked

    for z in range(0, len(circles)):
        #checks if a circle was clicked and that circle hasn't already been clicked
        #this is what I get for putting lists inside of lists
        if event.x in list(range((circles[z])[0], (circles[z])[0]+30)) and \
           event.y in list(range((circles[z])[1], (circles[z])[1]+30)) and \
           z not in clicked:

            #if this is the first click, no lines are drawn yet 
            if last != None:
                newLine=canvas.create_line((circles[last])[0]+15, (circles[last])[1]+15, \
                    (circles[z])[0]+15, (circles[z])[1]+15)
                #line drawn below circles
                canvas.tag_lower(newLine)
                tk.update()

            #could read last item of list instead of var, but that makes it more complicated
            last=z
            clicked.append(z)

    if len(clicked) == score+4:
        level_complete(circles, clicked, canvas)


def create_level(canvas, score):
    #reset
    global clicked, last, circles, text
    clicked, circles, text=[],[],[]
    last=None

    #creates circle coordinates than puts them on canvas
    for z in range(0, score+4):
        x=random.randint(10, 660)
        y=random.randint(10, 460)
        #Repeats if there is already a circle too close (keep in mind that values are for the top left corner)
        while not len(canvas.find_overlapping(x-20, y-20, x+50, y+50)) == 0:
            x=random.randint(10, 660)
            y=random.randint(10, 460)

        canvas.create_oval(x, y, x+30, y+30, fill='lightblue')
        text.append(canvas.create_text(x+32, y+32, text=z+1))

        circles.append([x,y])
        
    tk.update()
    #4/5 second to memorize per num  (can change decimal)
    time.sleep((score+4)*0.8)
    
    #hides all of the text
    for item in text:
        canvas.itemconfigure(item, state='hidden')

canvas.bind_all('<ButtonRelease-1>', line)
create_level(canvas, score)
mainloop()