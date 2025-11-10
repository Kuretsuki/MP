from argparse import ArgumentParser
from termcolor import colored
from game_display import load_mapp, clear, TILE_EMOJIS
from items_functionality import burn_trees, cut_tree
from map_tracking import mapp, finding_L, finding_items, mushroom_counter

collected_mush = [0]
total_mush = [0]

def implement_game(filename, moves = None, output_file = None):
    directions = {
        "W":(-1, 0), 
        "A": (0, -1), 
        "S":(1, 0), 
        "D":(0, 1),
        "P":(0, 0),
        "!":(0, 0)
    }

    clear()
    status = "NO CLEAR"
    # Item-related variables
    pick_up_message = ""
    held_items = None
    axes_loc = finding_items(mapp(filename))[0]
    fires_loc = finding_items(mapp(filename))[1]

    # User-interaction-related variables
    previous_loc = "."
    current_loc = finding_L(mapp(filename))

    # End-state-deciding variables
    current_mush = 0
    collected_mush = [current_mush]
    mushrooms = mushroom_counter(mapp(filename))
    
    # Display-related variables
    grid = [list(row) for row in mapp(filename)]
    first_display = ["".join(row) for row in grid]

    if moves is not None:
        moves = list(moves.upper())
    else:
        clear()
        load_mapp(first_display)


    while True:
        if moves is None:
            print()
            print(colored(f"{current_mush} ", "magenta") 
                + "out of " 
                + colored(f"{mushrooms} ", "magenta") 
                + "mushroom(s) collected")
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
                        print(colored(("There is an axe available for pickup!"), "yellow"))
                    else:
                        print(colored("This item is unavailable for pickup.", "red"))
                elif current_loc in fires_loc:
                    if not held_items:
                        print(colored("There is a flamethrower available for pickup!", "yellow"))
                    else:
                        print(colored("This item is currently unavailable for pickup.", "red"))
                else:
                    print("There is no item here.")


            if held_items == None:
                print("Currently not holding anything.")
            else:
                print(f"Currently holding {TILE_EMOJIS[held_items]}")


            # Getting input from user
            movements = input("What is your next move?: ").upper()
            if not movements:
                clear()
                partial_res = ["".join(row) for row in grid]
                load_mapp(partial_res)
                print()
                print(colored("Invalid move! Use W/A/S/D/P/!.", "red"))
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
                    print()
                    print(colored("Invalid move! Use W/A/S/D/P/!.", "red"))
                continue

            x = current_loc[0]
            y = current_loc[1]
            i, j = directions[movement]


            if movement == "P":
                clear() if moves is None else None
                if previous_loc in ["*", "x"] and not held_items:  # if may item sa pinuntahang tile
                    axes_loc.remove(current_loc) if previous_loc == "x" else fires_loc.remove(current_loc)
                    held_items = previous_loc
                    pick_up_message = colored("You picked up a flamethrower!", "yellow") if previous_loc == "*" else colored("You picked up an axe!", "yellow")
                    previous_loc = "."
                elif previous_loc not in ["*", "x"]:
                    pick_up_message = colored("There is no item to be picked up!", "red")
                else:
                    pick_up_message = colored(f"You are already holding an item!", "red")
                        
                grid[x][y] = "."  
                grid[x + i][y + j] = "L"
                current_loc = (x + i, y + j)
                clear() if moves is None else None
                partial_res = ["".join(row) for row in grid]
                load_mapp(partial_res)
                continue

            if movement == "!":
                return "RESET"

            if 0 <= x + i < len(grid) and 0 <= y + j < len(grid[x + i]):
                if grid[x + i][y + j] in [".", "_", "*", "x", "T"]: # if puwede daanan
                    if grid[x + i][y + j] == "T": # if tree
                        if held_items == "x":
                            cut_tree(grid, x + i, y + j)
                            held_items = None
                            pick_up_message = colored("You used an axe!", "yellow")
                        elif held_items == "*":
                            burn_trees(grid, x + i, y + j )
                            held_items = None
                            pick_up_message = colored("You used a flamethrower!", "yellow")
                        else:
                            clear() if moves is None else None
                            partial_res = ["".join(row) for row in grid]
                            if moves is None:
                                load_mapp(partial_res)
                                print(colored("\nThere's a tree blocking your path!", "red"))
                            continue

                    grid[x][y] = previous_loc
                    previous_loc = grid[x + i][y + j]
                    grid[x + i][y + j] = "L"
                    current_loc = (x + i, y + j) 
                    if moves is None:
                        partial_res = ["".join(row) for row in grid]
                        clear()
                        load_mapp(partial_res)
                
                if grid[x + i][y + j] == "R": # if rock
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
                        partial_res = ["".join(row) for row in grid]
                        clear()
                        load_mapp(partial_res)
                        print(colored("You're not strong enough to push the rocks!", "red"))
                        continue
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
                            clear()
                            load_mapp(partial_res)
                            print(colored("\nCongratulations!", "yellow"))
                            print(f"\n{mushrooms} out of {mushrooms} mushroom(s) collected\n")
                            return True 
                        else:
                            status = "CLEAR"
                        break

                elif grid[x + i][y + j] == "~":
                    grid[x][y] = "."
                    current_loc = (x + i, y + j)
                    partial_res = ["".join(row) for row in grid]
                    collected_mush = current_mush
                    clear() if moves is None else None
                    load_mapp(partial_res)
                    if moves is None:
                        print(colored("\nGame Over!", "red"))
                        print(colored("You fell in the water!"))
                        print(f"\n{collected_mush} out of {mushrooms} mushroom(s) collected\n")
                        
                    if output_file:
                        with open(output_file, "w", encoding="utf-8") as f:
                            f.write("NO CLEAR\n")
                            for row in grid:
                                f.write("".join(row) + "\n")

                    return False
            else:
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
    return status
