print('Answer \'true\' or \'false\' to each question.')
print('Credits: Buzzfeed, Muse Magazine, Weird but True\n')

gamemode=int(input('Version (1, 2, or 3):  '))
if gamemode == 1:
    file=open('Questions.txt')
elif gamemode == 2:
    file=open('Questions 2.txt')
else:
    file=open('Questions 3.txt')
txt=file.readlines()   
file.close() 
print()

#Figure out the line numbers with questions
q_numbers=list(range(0,len(txt),2))

score=0
#10 is the number of questions
for x in range(10):
    print(txt[q_numbers[x]])
    user_a=input('True or False?  ')

    if txt[2*x+1] == user_a:
        print('Correct!\n')
        score += 1
    else:
        print('Incorrect.\n')

print('Score: %s%' %(score))
