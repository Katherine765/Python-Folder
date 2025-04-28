def is_valid(grid, r, c, n):
    not_in_row = n not in grid[r]
    not_in_column = n not in [grid[i][c] for i in range(9)]
    not_in_box = n not in [grid[i][j] for i in range(r//3*3, r//3*3+3) for j in range(c//3*3, c//3*3+3)]
    return not_in_row and not_in_column and not_in_box


def solve(grid, r=0, c=0):
    if r == 9:
        return True
    elif c == 9:
        return solve(grid, r+1, 0)
    elif grid[r][c] != 0:
        return solve(grid, r, c+1)
    else:
        for n in range(1, 10):
            if is_valid(grid, r, c, n):
                grid[r][c] = n
                if solve(grid, r, c+1):
                    return True
                grid[r][c] = 0
        return False
    
    
grid = [ [0,0,0,0,0,0,5,7,3],
         [8,0,0,0,2,0,0,0,0],
         [7,0,0,9,0,0,8,1,0],
         [5,8,0,7,0,6,0,0,0],
         [0,0,1,8,0,0,0,6,0],
         [2,3,0,0,4,0,0,0,9],
         [9,1,5,0,0,0,0,0,0],
         [0,0,0,0,8,0,6,0,1],
         [0,0,0,0,0,0,0,4,0] ]
solve(grid)
print(*grid, sep='\n')