grid = [
    "████████████████████████████",
    "█       ██████        █    █",
    "█       █    █        █    █",
    "█       █    █        █    █",
    "█████████    █████████     █",
    "█                          █",
    "█   ████████████   ██████  █",
    "█   █          █   █    █  █",
    "█   █          █   █    █  █",
    "████████████████████████████",
    "█    █         █           █",
    "█    █         █           █",
    "█    ███████████           █",
    "█                          █",
    "████████████████████████████"
]


def display(grid):
    for string in grid:
        print(string)
            

def flood_fill(grid, x, y):
    if grid[y][x] == '█':
        return grid
    
    result = grid[:]
    result[y] = result[y][:x] + '█' + result[y][x+1:]
    for (x2, y2) in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
        result = flood_fill(result, x2, y2)

    return result

display(grid)
print()
display(flood_fill(grid, 25, 1))




