import random  

class Die:           #creates the die class
    def __init__(self, faceValue=0, face=''):     #makes the faceValue and face variables
       self.faceValue = faceValue
       self.face = face
    def roll(self):
        self.faceValue=random.randint(1,6)      #"rolls" the die
        if self.faceValue==1:
            self.face=' -------\n|       |\n|   o   |\n|       |\n -------'   #detects what the number is and sets the face to the appropriate image
        elif self.faceValue==2:
            self.face=' -------\n|  o    |\n|       |\n|    o  |\n -------'
        elif self.faceValue==3:
            self.face=' -------\n|  o    |\n|   o   |\n|    o  |\n -------'
        elif self.faceValue==4:
            self.face=' -------\n|  o o  |\n|       |\n|  o o  |\n -------'
        elif self.faceValue==5:
            self.face=' -------\n|  o o  |\n|   o   |\n|  o o  |\n -------'
        else:
            self.face=' -------\n|  o o  |\n|  o o  |\n|  o o  |\n -------'
    def __str__(self):
        return self.face  #returns the image


