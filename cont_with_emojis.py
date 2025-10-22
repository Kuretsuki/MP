import os

TILE_EMOJIS = {
    "T": "🌲",  # tree
    ".": "  ",  # empty tile
    "+": "🍄",  # mushroom
    "R": "🪨",  # rock
    "~": "💧",  # water
    "-": "⬜",  # paved
    "x": "🪓",  # axe
    "*": "🔥",  # flamethrower
    "L": "🧑",  # Laro Craft (player)
}

def load_mapp(mapp):
    for row in mapp:
        emoji_row = [TILE_EMOJIS.get(tile, tile) for tile in row]
        print("".join(emoji_row))


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

def implement_game(filename): # updating map for each move ni user
    directions = {
        "W":(-1, 0), 
        "A": (0, -1), 
        "S":(1, 0), 
        "D":(0, 1)
    }
    clear()
    current_loc = finding_L(mapp(filename))
    grid = [list(row) for row in mapp(filename)]
    first_display = ["".join(row) for row in grid]
    mushrooms = mushroom_counter(mapp(filename))
    current_mush = 0
    load_mapp(first_display)
    while True:
        print(f"{current_mush} out of {mushrooms} mushroom(s) collected")
        print()
        print("[W] Move up")
        print("[A] Move left")
        print("[S] Move down")
        print("[D] Move right")
        print("[!] Reset")
        print()
        movement = input("What is your next move?: ").upper()
        if movement not in directions:
            clear()
            partial_res = ["".join(row) for row in grid]
            load_mapp(partial_res)
            print("Invalid move! Use W/A/S/D/P/!.")
            continue
        x = current_loc[0]
        y = current_loc[1]
        i, j = directions[movement]
        if 0 <= x + i <= len(grid) and 0 <= y + j <= len(grid[0]):  
            if grid[x + i][y + j] == ".": # if puwede daanan
                grid[x + i][y + j] = "L"
                grid[x][y] = "."
                current_loc = (x + i, y + j) 
                partial_res = ["".join(row) for row in grid]
                clear()
                load_mapp(partial_res)

            elif grid[x + i][y + j] == "T":
                clear()
                partial_res = ["".join(row) for row in grid]
                load_mapp(partial_res)
            elif grid[x + i][y + j] == "R":
                if grid[x + 2*i][y + 2*j] ==".":
                    grid[x + 2*i][y + 2*j] = "R"
                    grid[x + i][y + j] = "L"
                    grid[x][y] = "."
                    current_loc = (x + i, y + j)
                elif grid[x + 2*i][y + 2*j] == "~":
                    grid[x + 2*i][y + 2*j] = "-"
                    grid[x + i][y + j] = "L"
                    grid[x][y] = "."
                    current_loc = (x + i, y + j)
                elif grid[x + 2*i][y + 2*j] == "-":
                    grid[x + 2*i][y + 2*j] = "R"
                    grid[x + i][y + j] = "L"
                    grid[x][y] = "."
                    current_loc = (x + i, y + j)
                else:
                    partial_res = ["".join(row) for row in grid]
                    clear()
                    load_mapp(partial_res)
                partial_res = ["".join(row) for row in grid]
                clear()
                load_mapp(partial_res)

            elif grid[x + i][y + j] == "-":
                grid[x + i][y + j] = "L"
                grid[x][y] = "."
                current_loc = (x + i, y + j)
                partial_res = ["".join(row) for row in grid]
                clear()
                load_mapp(partial_res)

            elif grid[x + i][y + j] == "+":
                current_mush += 1
                grid[x + i][y + j] = "L"
                grid[x][y] = "."
                current_loc = (x + i, y + j)
                partial_res = ["".join(row) for row in grid]
                clear()
                load_mapp(partial_res)

                if current_mush == mushrooms:
                    partial_res = ["".join(row) for row in grid]
                    clear()
                    print("You Win!")
                    print(f"You collected all {mushrooms} mushrooms! 🍄🏆")
                    break

            elif grid[x + i][y + j] == "~":
                grid[x + i][y + j] = "L"
                grid[x][y] = "."
                clear()
                load_mapp(partial_res)
                print("You fell in the water!")
                break


                    

if __name__ == "__main__":
    implement_game("testmap.txt")
