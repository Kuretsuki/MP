from termcolor import colored
from game_display import load_mapp, clear
from items_functionality import burn_trees, cut_tree
import time

def handle_pickup(previous_loc, current_loc, axes_loc, fires_loc, held_items, grid):
    pick_up_message = ""
    x, y = current_loc

    if previous_loc in ["*", "x"] and not held_items:
        # Pick up available item
        if previous_loc == "x":
            if current_loc in axes_loc:
                axes_loc.remove(current_loc)
            held_items = previous_loc
            pick_up_message = colored("You picked up an axe!", "yellow")
        else:
            if current_loc in fires_loc:
                fires_loc.remove(current_loc)
            held_items = previous_loc
            pick_up_message = colored("You picked up a flamethrower!", "yellow")
        previous_loc = "."
    elif previous_loc not in ["*", "x"]:
        pick_up_message = colored("There is no item to be picked up!", "red")
    else:
        pick_up_message = colored("You are already holding an item!", "red")

    grid[x][y] = "L"
    return previous_loc, held_items, pick_up_message


def handle_movement(grid, x, y, i, j, held_items, previous_loc, current_mush, mushrooms, multi_move = False):
    current_loc = (x, y)
    next_x, next_y = x + i, y + j
    pick_up_message = ""
    delay = True

    # Checking if movement is within map bounds
    if not (0 <= next_x < len(grid) and 0 <= next_y < len(grid[0])):
        partial_res = ["".join(row) for row in grid]
        clear()
        load_mapp(partial_res)
        print(colored("\nYou cannot move outside the map!", "red"))
        return (x, y), previous_loc, held_items, current_mush, None, pick_up_message

    target_cell = grid[next_x][next_y]

    # Moving on a valid tile
    if target_cell in [".", "_", "*", "x", "T"]:
        if target_cell == "T":  # Tree interaction
            if held_items == "x":
                cut_tree(grid, next_x, next_y)
                held_items = None
                pick_up_message = colored("You used an axe!", "yellow")
            elif held_items == "*":
                burn_trees(grid, next_x, next_y)
                held_items = None
                pick_up_message = colored("You used a flamethrower!", "yellow")
            else:
                partial_res = ["".join(row) for row in grid]
                clear()
                load_mapp(partial_res)
                print(colored("\nThere's a tree blocking your path!", "red"))
                return (x, y), previous_loc, held_items, current_mush, None, pick_up_message

        grid[x][y] = previous_loc
        previous_loc = grid[next_x][next_y]
        grid[next_x][next_y] = "L"
        clear()
        load_mapp(["".join(row) for row in grid])

        if delay and multi_move:
            time.sleep(0.25)

        return (next_x, next_y), previous_loc, held_items, current_mush, None, pick_up_message

    # Pushing rocks
    elif target_cell == "R":
        next_two_x, next_two_y = x + 2*i, y + 2*j
        if not (0 <= next_two_x < len(grid) and 0 <= next_two_y < len(grid[0])):
            partial_res = ["".join(row) for row in grid]
            clear()
            load_mapp(partial_res)
            print(colored("\nYou can't push the rock off the map!", "red"))
            return (x, y), previous_loc, held_items, current_mush, None, pick_up_message

        next_cell = grid[next_two_x][next_two_y]

        # If rock is pushed on an empty tile
        if next_cell == ".":
            grid[next_two_x][next_two_y] = "R"
            grid[next_x][next_y] = "L"
            grid[x][y] = "."
            current_loc = (next_x, next_y)

        # If rock is pushed in the water
        elif next_cell == "~":
            grid[next_two_x][next_two_y] = "_"
            grid[next_x][next_y] = "L"
            grid[x][y] = "."
            current_loc = (next_x, next_y)

        # If rock is pushed on a paved-tile
        elif next_cell == "_":
            grid[next_two_x][next_two_y] = "R"
            grid[next_x][next_y] = "L"
            grid[x][y] = "."
            current_loc = (next_x, next_y)

        # If rock is pushed on a tree or mushroom
        elif next_cell in ["T", "+"]:
            partial_res = ["".join(row) for row in grid]
            obstacle = "tree" if next_cell == "T" else "mushroom"
            clear()
            load_mapp(partial_res)
            print(colored(f"\nThere's a {obstacle} blocking your path!", "red"))
            return (x, y), previous_loc, held_items, current_mush, None, pick_up_message

        # If two or more rock is pushed 
        elif next_cell == "R":
            partial_res = ["".join(row) for row in grid]
            clear()
            load_mapp(partial_res)
            print(colored("\nYou're not strong enough to push multiple rocks!", "red"))
            return (x, y), previous_loc, held_items, current_mush, None, pick_up_message

        clear()
        load_mapp(["".join(row) for row in grid])
        if delay and multi_move:
            time.sleep(0.15)

        return current_loc, previous_loc, held_items, current_mush, None, pick_up_message

    # Collecting mushrooms
    elif target_cell == "+":
        current_mush += 1
        grid[x][y] = previous_loc
        previous_loc = "."
        grid[next_x][next_y] = "L"
        current_loc = (next_x, next_y)
        clear()
        load_mapp(["".join(row) for row in grid])

        # Collected all mushrooms - Winning state
        if current_mush == mushrooms:
            print(colored("\nCongratulations!", "yellow"))
            print(f"\n{mushrooms} out of {mushrooms} mushroom(s) collected\n")
            return current_loc, previous_loc, held_items, current_mush, True, pick_up_message
        else:

            return current_loc, previous_loc, held_items, current_mush, None, pick_up_message

    # Falling in the water - Losing State
    elif target_cell == "~":
        grid[x][y] = "."
        current_loc = (next_x, next_y)
        clear()
        load_mapp(["".join(row) for row in grid])
        print(colored("\nGame Over!", "red"))
        print(colored("You fell in the water!"))
        print(f"\n{current_mush} out of {mushrooms} mushroom(s) collected\n")
        return current_loc, previous_loc, held_items, current_mush, False, pick_up_message