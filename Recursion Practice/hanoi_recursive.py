N = 6

towers = [[n for n in range(N-1,-1,-1)],[],[]]

def move_ring(S,E):
    towers[E].append(towers[S].pop())

def solve(N,S,T,E):
    if N < 2:
        move_ring(S,E)
        return
    
    solve(N-1,S,E,T)
    move_ring(S,E)
    solve(N-1,T,S,E)

print(towers)
solve(N,0,1,2)
print(towers)