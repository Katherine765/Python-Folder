from Dice import Die
die=Die()

print('type "q" to quit')
while True:
    total=0
    number=input('Number of dice:  ')
    if number == 'q':
        break
    else:
        print()
        for x in range (0, int(number)):
            die.roll()
            print(die)
            total=total+die.faceValue
        print('Total: %s\n' %total)

    
