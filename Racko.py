import random

# decks
deck = list(range(60))
random.shuffle(deck)
discard = []

# players' boards
p1 = [deck.pop(-1) for _ in range(10)]
p2 = [deck.pop(-1) for _ in range(10)]

# lists of cards in good positions and gaps in between
ok=[(i,card) for i, card in enumerate(p2) if i == card//6] # each okay item holds (place in board, card number)
gaps = []

# displays a given player's board including visualization
def display(player):
    for i in range(9,-1,-1):
        value = player[i]
        print(f' {i}|    {value} '+'.'*(value//3) if value < 10 else f' {i}|    {value}'+'.'*(value//3))


# user
def p1_turn():
    display(p1)
    if discard:
        seen = discard[-1]
        card = seen if input(f'{seen} or deck?  ')==str(seen) else deck.pop(-1)
    else:
        card = deck.pop(-1)

    place = input(f'placement of {card}:  ')

    # if you don't input correctly it will just discard
    if place.isdigit() and int(place) in range(10):
        place = int(place)
        discard.append(p1[place])
        p1[place] = card
    else:
        discard.append(card)
        
    print()

# find the gaps between the acceptably placed cards        
def define_gaps(ok):
    if not ok:
        return (range(10),range(60))
    
    gaps = []

    #first gap 
    if ok[0][0] > 0: # unless the placement of the first ok card is already the first spot
        gaps.append((range(0, ok[0][0]), range(0, ok[0][1])))

    # all the other gaps start after an appropriately placed card
    # the iteration gives the start of the gap, and inside the loop finds where it ends
    for i, pair in enumerate(ok[:-1]):
        indexes = range(pair[0]+1,ok[i+1][0])
        values  = range(pair[1]+1,ok[i+1][1])
        if len(indexes) > 0:
            gaps.append((indexes,values))
    
    #last gap needs to be done separately because there is no appropriately placed card after the last gap to be used in the loop
    if ok[-1][0] < 9:
        gaps.append((range(ok[-1][0] +1, 10), range(ok[-1][1] +1, 60)))
                                      
    return gaps

# find the range that a card falls into
def get_gap(card, gaps):
    for i, pair in enumerate(gaps):
        if card in pair[1]:
            return pair
    return False

def p2_turn(ok):
    ok.sort(key = lambda x : x[0])
    gaps = define_gaps(ok)

    # if the top discard fits into one of the gaps just use htat
    seen = discard[-1]
    gap = get_gap(seen, gaps)
    if gap:
        card = seen
    else:
        card = deck.pop(-1)
        gap = get_gap(card, gaps)

    if gap:
        relative_num = card - gap[1][0] # subtracts the start value of the gap
        spacing = len(gap[1])/len(gap[0])
        place = int(relative_num//spacing + gap[0][0]) # re-adds the start value of the gap
        discard.append(p2[place])
        p2[place] = card
        ok.append((place, card))
    else:
        # this is something i could improve if i wanted
        discard.append(card)    
            
    print('computer')
    display(p2)
    print()
 
while True:
    print('you')
    p1_turn()
    if p1 == sorted(p1):
        break
    p2_turn(ok)
    if p2 == sorted(p2):
        break
