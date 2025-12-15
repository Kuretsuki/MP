from classes import Interactive
from game_display import load_mapp, clear, TILE_EMOJIS
from termcolor import colored

def implement_game(filename="testmap.txt"):
    """
    Runs the main game loop for a single level/map.

    Initializes the game state based on the provided map file, handles user 
    input for movement and actions, updates the display, and tracks the 
    win/loss condition.

    Args:
        filename (str, optional): The path to the map file to load. Defaults to "testmap.txt".

    Returns:
        bool or str: 
            - True if the player wins (collects all mushrooms).
            - False if the player loses (falls in water).
            - "RESET" if the player chooses to restart the level.
            - "QUIT" if the player chooses to exit to the main menu.
    """
    game = Interactive(filename)

    clear()
    first_display = ["".join(row) for row in game.playing_map] 
    load_mapp(first_display)
    while game.state is None:
        print(colored(f"\n{game.current_mushroom} ", "magenta") +
          "out of " + colored(f"{game.mushroom_count} ", "magenta") +
          " mushroom(s) collected\n")
        print("[W] Move up\n[A] Move left\n[S] Move down\n[D] Move right\n[P] Pick up\n[!] Reset\n")

        if game.pick_up_message:
            print(game.pick_up_message)
            game.pick_up_message = ""
        else:
            if game.player_loc in game.axes_loc:
                print(colored("There is an axe available for pickup!", "yellow")
                      if not game.held_items else colored("This item is unavailable for pickup.", "red"))
            elif game.player_loc in game.fires_loc:
                print(colored("There is a flamethrower available for pickup!", "yellow")
                      if not game.held_items else colored("This item is currently unavailable for pickup.", "red"))
            else:
                print("There is no item here.")
        print(f"Currently holding {TILE_EMOJIS[game.held_items]}" if game.held_items else "Currently not holding anything.")

        move = input("What is your next move?: ")
        if not move:
                clear()
                load_mapp(["".join(row) for row in game.playing_map])
                print(colored("\nInvalid move! Use W/A/S/D/P/!/Q.", "red"))
                continue
        for m in move:
            if m.upper() not in game.directions:
                clear()
                partial_res = ["".join(row) for row in game.playing_map]
                load_mapp(partial_res)
                print()
                print(colored("Invalid move! Use W/A/S/D/P/!.", "red"))
                break

            if m.upper() == "P":
                game.handle_pickup()
                clear()
                load_mapp(["".join(row) for row in game.playing_map])
                continue
            elif m == "!":
                return "RESET"
            elif m == "Q":
                clear()
                load_mapp(["".join(row) for row in game.playing_map])
                return "QUIT"
            else:
                game.handle_movement(m, multi_move = (len(move) > 1))

        if game.state in (True, False):
            return game.state
