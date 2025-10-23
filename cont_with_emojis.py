import os

TILE_EMOJIS = {
    "T": "🌲",  # tree
    ".": "  ",  # empty tile
    "+": "🍄",  # mushroom
    "R": "🪨",  # rock
    "~": "🟦",  # water
    "_": "🟥",  # paved
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

def finding_items(tups):
    r = len(tups)
    c = len(tups[0]) if r else 0
    grid = [list(row) for row in tups]
    directions = [(1,0), (-1,0)]
    axe = []
    fire = []

    for i in range(r):
        for j in range(c):
            if grid[i][j] == "x":
                axe.append((i, j))
            elif grid[i][j] == "*":
                fire.append((i ,j))
    return (axe, fire)

def burn_trees(grid, x, y):
    if not (0 <= x < len(grid) and 0 <= y < len(grid[0])):
        return
    if grid[x][y] != "T":
        return
    grid[x][y] = "." # burned trees turns to empty
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
        burn_trees(grid, x + dx, y + dy)


def implement_game(filename): # updating map for each move ni user
    directions = {
        "W":(-1, 0), 
        "A": (0, -1), 
        "S":(1, 0), 
        "D":(0, 1),
        "P":(0, 0)
    }

    clear()
    pick_up_message = ""
    held_items = None
    previous_loc = "."
    current_loc = finding_L(mapp(filename))
    axes_loc = finding_items(mapp(filename))[0]
    fires_loc = finding_items(mapp(filename))[1]
    grid = [list(row) for row in mapp(filename)]
    first_display = ["".join(row) for row in grid]
    current_mush = 0
    mushrooms = mushroom_counter(mapp(filename))
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
        
        if pick_up_message:  
            print(pick_up_message)
            pick_up_message = ""
        else:
            if current_loc in axes_loc:
                if not held_items:
                    print("There is an axe available for pickup!")
                else:
                    print("This item is unavailable for pickup.")
            elif current_loc in fires_loc:
                if not held_items:
                    print("There is a flamethrower available for pickup!")
                else:
                    print("This item is currently uavailable for pickup.")
            else:
                print("There is no item here.")


        if held_items == None:
            print("Currently not holding anything.")
        else:
            print(f"Currently holding {TILE_EMOJIS[held_items]}")



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


        if movement == "P":
            clear()
            if previous_loc in ["*", "x"] and not held_items:  # if may item sa pinuntahang tile
                axes_loc.remove(current_loc) if previous_loc == "x" else fires_loc.remove(current_loc)
                held_items = previous_loc
                pick_up_message = "You picked up a flamethrower!" if previous_loc == "*" else "You picked up an axe!"
                previous_loc = "."
            elif previous_loc not in ["*", "x"]:
                pick_up_message = "There is no item to be picked up!"

            else:
                pick_up_message = f"You are alreading holding an item!"
                    
            grid[x][y] = "."  
            grid[x + i][y + j] = "L"
            current_loc = (x + i, y + j)
            partial_res = ["".join(row) for row in grid]

            load_mapp(partial_res)

            

        if 0 <= x + i < len(grid) and 0 <= y + j < len(grid[0]):
            if grid[x + i][y + j] in [".", "_", "*", "x", "T"]: # if puwede daanan
                if grid[x + i][y + j] == "T": # if tree
                    if held_items == "x":
                        grid[x + i][y + j] = "."
                        held_items = None
                        pick_up_message = "You used an axe!"
                    elif held_items == "*":
                        burn_trees(grid, x + i, y + j )
                        held_items = None
                        pick_up_message = "You used a flamethrower!"
                    else:
                        clear()
                        partial_res = ["".join(row) for row in grid]
                        load_mapp(partial_res)
                        continue

                grid[x][y] = previous_loc
                previous_loc = grid[x + i][y + j]
                grid[x + i][y + j] = "L"
                current_loc = (x + i, y + j) 
                partial_res = ["".join(row) for row in grid]
                clear()
                load_mapp(partial_res)
            
            elif grid[x + i][y + j] == "R": # if rock
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
                    partial_res = ["".join(row) for row in grid]
                    clear()
                    load_mapp(partial_res)
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
                    load_mapp(partial_res)
                    print("You Win!")
                    break

            elif grid[x + i][y + j] == "~":
                grid[x + i][y + j] = "L"
                grid[x][y] = "."
                current_loc = (x + i, y + j)
                partial_res = ["".join(row) for row in grid]
                clear()
                load_mapp(partial_res)
                print("You fell in the water!")
                break


implement_game("testmap.txt")
