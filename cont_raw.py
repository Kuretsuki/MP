import os

TILE_EMOJIS = {
    "T": "🌲",  # tree
    ".": "  ",  # empty tile
    "+": "🍄",  # mushroom
    "R": "🪨",  # rock
    "~": "💧",  # water
    "-": "⬛",  # paved
    "x": "🪓",  # axe
    "*": "🔥",  # flamethrower
    "L": "🧑",  # Laro Craft (player)
}


def finding_L(tups): # current location ni user
    r = len(tups)
    c = len(tups[0]) if r else 0
    grid = [list(row) for row in tups]
    directions = [(1,0), (-1,0)]

    for i in range(r):
        for j in range(c):
            if grid[i][j] == "L":
                return (i, j)


def mushroom_counter(tups): # counter ng mushrooms
    r = len(tups)
    c = len(tups[0]) if r else 0
    grid = [list(row) for row in tups]
    total_mushrooms = 0
    for i in range(r):
        for j in range(c):
            if grid[i][j] == "+":
                total_mushrooms += 1
    return total_mushrooms
                

def mapp(filename): # turned map into list
    with open(filename) as f:
        data = f.read().splitlines()
    return data



def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def movements(filename): # updating map for each move ni user
    directions = {
        "W":(-1, 0), 
        "A": (0, -1), 
        "S":(1, 0), 
        "D":(0, 1)
    }
    current_loc = finding_L(mapp(filename))
    grid = [list(row) for row in mapp(filename)]
    while True:
        movement = input("What is your next move?: ").upper()
        x = current_loc[0]
        y = current_loc[1]
        i, j = directions[movement]
        if 0 < x + i < len(grid) and 0 < y + j < len(grid[0]):
            current_mush = 0
            if grid[x + i][y + j] == ".":
                grid[x + i][y + j] = "L"
                grid[x][y] = "."
                current_loc = (x + i, y + j) 
                clear()
                print("\n".join(row for row in ["".join(row) for row in grid]))
            elif grid[x + i][y + j] == "T":
                clear()
                print("\n".join(row for row in ["".join(row) for row in grid]))
                pass
            elif grid[x + i][y + j] == "R":
                if grid[x + 2*i][y + 2*j] ==".":
                    grid[x + 2*i][y + 2*j] = "R"
                    grid[x + i][y + j] = "L"
                    grid[x][y] = "."
                    current_loc = (x + i, y + j)
                elif grid[x + 2*i][y + 2*j] == "~":
                    grid[x + 2*i][y + 2*j] = "_"
                    grid[x + i][y + j] = "L"
                    grid[x][y] = "."
                    current_loc = (x + i, y + j)
                elif grid[x + 2*i][y + 2*j] == "_":
                    grid[x + 2*i][y + 2*j] = "R"
                    grid[x + i][y + j] = "L"
                    grid[x][y] = "."
                    current_loc = (x + i, y + j)
                else:
                    pass
                clear()
                print("\n".join(row for row in ["".join(row) for row in grid]))
            elif grid[x + i][y + j] == "+":
                mushrooms = mushroom_counter(mapp(filename))
                current_mush += 1
                grid[x + i][y + j] = "L"
                grid[x][y] = "."
                current_loc = (x + i, y + j)
                clear()
                print("\n".join(row for row in ["".join(row) for row in grid]))

                if current_mush == mushrooms:
                    clear()
                    print("\n".join(row for row in ["".join(row) for row in grid]))
                    break
            elif grid[x + i][y + j] == "_":
                grid[x + i][y + j] = "L"
                grid[x][y] = "."
                current_loc = (x + i, y + j)
                clear()
                print("\n".join(row for row in ["".join(row) for row in grid]))
                
    
print(movements("testmap.txt"))


