disk_count  = int(input('Disks:  '))-1
#r because it is used for ranges
disk_count_r = disk_count+1
print()

disks = {}
#don't turn this into disk_count_r (PEMDAS)
blank = ' '* (2*disk_count+1)
for x in range(disk_count_r):
    buffer = disk_count-x
    disks[x] = ' '*buffer + '*'*(2*x+1) + ' '*buffer

A =[disks[x] for x in range(disk_count_r)]
B =[blank for _ in range(disk_count_r)]
C =[blank for _ in range(disk_count_r)]


buffer = ' '*(disk_count)
def display_board():
    for x in range(disk_count_r):
        print(A[x]+B[x]+C[x])
    print(buffer+'A'+buffer*2+'B'+buffer*2+'C'+buffer)


def update(start_tower, end_tower):
    #finds place of top ring within the start tower
    old_index = None
    for spot, disk in enumerate(start_tower):
        old_index=spot
        if disk != blank:
            break

    #finds first blank spot within the end tower, starting from the bottom
    new_index = None
    for spot, disk in enumerate(reversed(end_tower)):
        new_index = disk_count-spot
        if disk == blank:
            break

    #makes sure the disk is on top of a bigger disk
    #if the first part of the or statement is met, the or short circuits which prevents an out of range error
    if (start_tower[old_index] != blank
        and (new_index == disk_count
        or len(start_tower[old_index].strip()) < len(end_tower[new_index+1].strip()))):
        
        #i do not understand how this edits the actual A, B, and C lists but it does
        end_tower[new_index] = start_tower[old_index]
        start_tower[old_index] = blank
    else:
        print('no can do')
        
turns = 0
while True:
    display_board()
    print()
    #input move in form of ab, cb, etc
    move = input('Move:  ').upper()
    #this turns the string 'A' into the A list
    update(globals()[move[0]], globals()[move[1]])
    turns +=1
    if not blank in C:
        display_board()
        #i googled the equation there
        print('You win in %s moves. %s was the minimum required.' %(turns,2**disk_count_r-1))
        break
