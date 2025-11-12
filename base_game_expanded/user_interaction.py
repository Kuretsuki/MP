from termcolor import colored
from game_display import load_mapp, clear, TILE_EMOJIS
from map_tracking import mapp, finding_L, finding_items, mushroom_counter
from game_main_controls import handle_pickup, handle_movement
import time

def implement_game(filename, moves = None, output_file = None, silent = False): 
    directions = {
        "W": (-1, 0),
        "A": (0, -1),
        "S": (1, 0),
        "D": (0, 1),
        "P": (0, 0),
        "!": (0, 0)
    }

    # State-related variables
    clear()
    status = "NO CLEAR"
    pick_up_message = ""
    held_items = None

    # Location-related variables
    previous_loc = "."
    current_loc = finding_L(mapp(filename))
    axes_loc, fires_loc = finding_items(mapp(filename))

    # Grid
    grid = [list(row) for row in mapp(filename)]

    # Mushroom-related variables
    mushrooms = mushroom_counter(mapp(filename))
    current_mush = 0

    # Start of the game
    first_display = ["".join(row) for row in grid]
    if moves is None and silent is False: 
        load_mapp(first_display)
    else:
        moves = list(moves.upper())

    while True:
        if moves is None:
            if silent is False:
                print(colored(f"\n{current_mush} ", "light_magenta") +
                  "out of " + colored(f"{mushrooms} ", "light_magenta") +
                  " mushroom(s) collected\n")
                print("[W] Move up\n[A] Move left\n[S] Move down\n[D] Move right\n[P] Pick up\n[!] Reset\n")

            if pick_up_message and silent is False:
                print(pick_up_message)
                pick_up_message = ""
            else:
                if silent is False:
                    if current_loc in axes_loc:
                        print(colored("There is an axe available for pickup!", "yellow")
                              if not held_items else colored("This item is unavailable for pickup.", "red"))
                    elif current_loc in fires_loc:
                        print(colored("There is a flamethrower available for pickup!", "yellow")
                              if not held_items else colored("This item is currently unavailable for pickup.", "red"))
                    else:
                        print("There is no item here.")
            if silent is False:
                print(f"Currently holding {TILE_EMOJIS[held_items]}" if held_items else "Currently not holding anything.")

            movements = input("What is your next move?: ").upper()
            if not movements and silent is False:
                clear()
                load_mapp(["".join(row) for row in grid])
                print(colored("\nInvalid move! Use W/A/S/D/P/!.", "red"))
                continue
            movement_list = list(movements)

        else:
            if not moves:
                break
            movement_list = [moves.pop(0)]

        for movement in movement_list:
            if movement not in directions:
                if moves is None and silent is False:
                    clear()
                    load_mapp(["".join(row) for row in grid])
                    print(colored("\nInvalid move! Use W/A/S/D/P/!.", "red"))
                else:
                    status = "NO CLEAR"
                movement_list = [] 
                break

            x, y = current_loc
            i, j = directions[movement]

            if movement == "P":
                previous_loc, held_items, pick_up_message = handle_pickup(
                    previous_loc, current_loc, axes_loc, fires_loc, held_items, grid)
                if moves is None and silent is False:
                    clear()
                    load_mapp(["".join(row) for row in grid])
                continue

            if movement == "!":
                return "RESET"

            current_loc, previous_loc, held_items, current_mush, state, pick_up_message = handle_movement(
                grid, x, y, i, j, held_items, previous_loc, current_mush, mushrooms,
                multi_move = (len(movement_list) > 1), silent = silent
            )

            if state is True:
                status = "CLEAR"
                break
            elif state is False:
                status = "NO CLEAR"
                break
                
        if moves is not None:
            partial_res = ["".join(row) for row in grid]
            if output_file:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(status + "\n")
                    for row in partial_res:
                        f.write(row + "\n")

        if state in (True, False):
            return status

    return status
