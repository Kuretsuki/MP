import os
import time
from argparse import ArgumentParser

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

collected_mush = [0]
total_mush = [0]

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
        for j in range(len(grid[i])):
            if grid[i][j] == "L":
                return (i, j)


def mushroom_counter(tups): # counter ng mushrooms
    r = len(tups)
    c = len(tups[0]) if r else 0
    grid = [list(row) for row in tups]
    total_mushrooms = 0
    for i in range(r):
        for j in range(len(grid[i])):
            if grid[i][j] == "+":
                total_mushrooms += 1
    return total_mushrooms           

def mapp(filename): # turned map into list
    if not os.path.exists(filename):
        print(f"Error: Map file '{filename}' not found!")
        exit(1)
    with open(filename, encoding = "utf=8") as f:
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
        for j in range(len(grid[i])):
            if grid[i][j] == "x":
                axe.append((i, j))
            elif grid[i][j] == "*":
                fire.append((i ,j))
    return (axe, fire)

def burn_trees(grid, x, y):
    if not (0 <= x < len(grid) and 0 <= y < len(grid[0])):
        return
    # stop if out of bounds
    if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[x]):
        return

    if grid[x][y] != "T":
        return

    grid[x][y] = "." # burned trees turns to empty
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        burn_trees(grid, x + dx, y + dy)

def implement_game(filename, moves = None, output_file = None): # updating map for each move ni user
    directions = {
        "W":(-1, 0), 
        "A": (0, -1), 
        "S":(1, 0), 
        "D":(0, 1),
        "P":(0, 0),
        "Q":(0, 0),
        "!":(0, 0)
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

    if moves is not None:
        moves = list(moves.upper())
    else:
        clear()
        load_mapp(first_display)

    status = "NO CLEAR"

    while True:
        if moves is None:
            print(f"{current_mush} out of {mushrooms} mushroom(s) collected")
            print()
            print("[W] Move up")
            print("[A] Move left")
            print("[S] Move down")
            print("[D] Move right")
            print("[!] Reset")
            print("[Q] Quit")
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
                        print("This item is currently unavailable for pickup.")
                else:
                    print("There is no item here.")


            if held_items == None:
                print("Currently not holding anything.")
            else:
                print(f"Currently holding {TILE_EMOJIS[held_items]}")


            # input from user
            movements = input("What is your next move?: ").upper()
            if not movements:
                clear()
                partial_res = ["".join(row) for row in grid]
                load_mapp(partial_res)
                print("Invalid move! Use W/A/S/D/P/!.")
                continue
            movement_list = list(movements)
        else:
            if not moves:
                break
            movement_list = [moves.pop(0).upper()]
            

        for movement in movement_list:
            if movement not in directions:
                if moves is None:
                    clear()
                    partial_res = ["".join(row) for row in grid]
                    load_mapp(partial_res)
                    print("Invalid move! Use W/A/S/D/P/!.")
                continue

            x = current_loc[0]
            y = current_loc[1]
            i, j = directions[movement]


            if movement == "P":
                if moves is None:
                    clear()
                else:
                    None
                if previous_loc in ["*", "x"] and not held_items:  # if may item sa pinuntahang tile
                    axes_loc.remove(current_loc) if previous_loc == "x" else fires_loc.remove(current_loc)
                    held_items = previous_loc
                    pick_up_message = "You picked up a flamethrower!" if previous_loc == "*" else "You picked up an axe!"
                    previous_loc = "."
                elif previous_loc not in ["*", "x"]:
                    pick_up_message = "There is no item to be picked up!"

                else:
                    pick_up_message = f"You are already holding an item!"
                        
                grid[x][y] = "."  
                grid[x + i][y + j] = "L"
                current_loc = (x + i, y + j)
                if moves is None:
                    partial_res = ["".join(row) for row in grid]
                    load_mapp(partial_res)
                continue

            if movement == "Q":
                partial_res = ["".join(row) for row in grid]
                collected_mush[0] = current_mush
                total_mush[0] = mushrooms
                if moves is None:
                    clear()
                    load_mapp(partial_res)
                    print("You quit the game.")

                if output_file:
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write("NO CLEAR\n")
                        for row in grid:
                            f.write("".join(row) + "\n")

                return False

            if movement == "!":
                return "RESET"

            if 0 <= x + i < len(grid) and 0 <= y + j < len(grid[x + i]):
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
                            clear() if moves is None else None
                            partial_res = ["".join(row) for row in grid]
                            if moves is None:
                                load_mapp(partial_res)
                            continue

                    grid[x][y] = previous_loc
                    previous_loc = grid[x + i][y + j]
                    grid[x + i][y + j] = "L"
                    current_loc = (x + i, y + j) 
                    if moves is None:
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
                    elif grid[x + 2*i][y + 2*j] == "R":
                        pass
                    if moves is None:
                        partial_res = ["".join(row) for row in grid]
                        clear()
                        load_mapp(partial_res)

                elif grid[x + i][y + j] == "+":
                    current_mush += 1
                    grid[x][y] = previous_loc   
                    previous_loc = "."        
                    grid[x + i][y + j] = "L"
                    current_loc = (x + i, y + j)
                    if moves is None:
                        partial_res = ["".join(row) for row in grid]
                        clear()
                        load_mapp(partial_res)

                    if current_mush == mushrooms:
                        if moves is None:
                            partial_res = ["".join(row) for row in grid]
                            clear()
                            load_mapp(partial_res)
                            print("You Win!")
                            return True
                        else:
                            status = "CLEAR"
                        break 

                elif grid[x + i][y + j] == "~":
                    grid[x][y] = "."
                    current_loc = (x + i, y + j)
                    partial_res = ["".join(row) for row in grid]
                    clear() if moves is None else None
                    load_mapp(partial_res)

                    # Print status message
                    if moves is None:
                        print("\033[31mGame Over!\033[0m")
                        print("You fell in the water!")
                        collected_mush[0] = current_mush
                        total_mush[0] = mushrooms
                    else:
                        print("NO CLEAR")

                    # Write to output file if provided
                    if output_file:
                        with open(output_file, "w", encoding="utf-8") as f:
                            f.write("NO CLEAR\n")
                            for row in grid:
                                f.write("".join(row) + "\n")

                    return False


            else:
                if moves is None:
                    partial_res = ["".join(row) for row in grid]
                    clear()
                    load_mapp(partial_res)

    if moves is not None:
        partial_res = ["".join(row) for row in grid]
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(status + "\n")
                for row in grid:
                    f.write("".join(row) + "\n")





def main_menu(): 
    print("==", "\033[31mShroom \033[33mRaider!\033[0m", "==")
    print("Press 1 to Play Game")
    print("Press 2 to View Leaderboard")
    print("Press 3 to Exit")
    return input("Choose an option: ")

def player_setup():
    name = input("Enter your username: ")
    return name

def save_score(name, time_taken, map_file):
    with open("leaderboard.txt", "a") as f:
        f.write(f"{map_file},{name},{time_taken}\n")

def load_leaderboard(map_file):
    scores = []
    if os.path.exists("leaderboard.txt"):
        with open("leaderboard.txt") as f:
            for line in f:
                entry_map, name, time_taken = line.strip().split(",")
                if entry_map == map_file:
                    scores.append((name, float(time_taken)))
    scores.sort(key=lambda x: x[1])
    return scores

def show_leaderboard(map_file):
    clear()
    scores = load_leaderboard(map_file)
    print("=== LEADERBOARDS ===")
    if not scores:
        print("No records yet!")
    else:
        for i, (name, t) in enumerate(scores[:10], start=1):
            print(f"{i}. {name} - {t:.2f} seconds")

    print("\nOptions:")
    print("[C] Clear Leaderboards")
    print("[Enter] Return to Menu")
    
    choice = input("Choose an option: ").strip().upper()

    if choice == "C":
        with open("leaderboard.txt", "w") as f:
            pass
        print("Leaderboard has been cleared!")
        input("Press Enter to continue...") 



def main():
    parser = ArgumentParser(description="Play Shroom Raider!")
    parser.add_argument("-f", "--stage_file", default="testmap.txt", help="Path to the stage file")
    parser.add_argument("-m", "--moves", default=None, help="String of moves to simulate (e.g., WASDP!Q)")
    parser.add_argument("-o", "--output", default=None, help="Output file for final map state")
    args = parser.parse_args()

    # AUTOMATED MODE
    if args.moves:
        # No print() here — fully silent
        result = implement_game(args.stage_file, moves=args.moves, output_file=args.output)
        while result == "RESET":
            result = implement_game(args.stage_file, moves=args.moves, output_file=args.output)
        return

    # INTERACTIVE MODE 
    while True:
        clear()
        choice = main_menu()
        if choice == "1":
            clear()
            name = player_setup()
            input(f"{name}, get ready to become a Shroom Raider!\nPress Enter to start the game...")
            start = time.time()
            result = implement_game(args.stage_file)
            while result == "RESET":
                result = implement_game(args.stage_file)
            end = time.time()
            duration = end - start
            if result:
                print(f"\n{name}, you finished in {duration:.2f} seconds!")
                save_score(name, duration, args.stage_file)
            else:
                print(f"You have collected {collected_mush[0]} out of {total_mush[0]} mushroom(s)")
                print(f"\n{name}, better luck next time!")
            input("\nPress Enter to return to menu...")
        elif choice == "2":
            show_leaderboard(args.stage_file)
        elif choice == "3":
            print("I am sure you'll be back...")
            break
        else:
            print("Invalid choice! Use 1/2/3.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()



