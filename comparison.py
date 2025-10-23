import os
import copy

emojis = {
    "T": "🌲",  # tree
    ".": "  ",  # empty tile
    "+": "🍄",  # mushroom
    "R": "🪨",  # rock
    "~": "💧",  # water
    "_": "⬛",  # paved (after rock sinks)
    "x": "🪓",  # axe (pickable)
    "*": "🔥",  # flamethrower (pickable)
    "L": "🧑",  # player
}

tiles = {
    "T": "a tree 🌲",
    ".": "empty ground",
    "+": "a mushroom 🍄",
    "R": "a rock 🪨",
    "~": "water 💧",
    "_": "a paved path ⬛",
    "x": "an axe 🪓",
    "*": "a flamethrower 🔥",
    "L": "yourself 🧑",
}

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def load_mapp(filename): # map into list
    with open(filename) as f:
        return f.read().splitlines()

def load_grid_from_mapp(mapp_lines):
    return [list(row) for row in mapp_lines]

def load_mapp_to_screen(mapp): # prints using emojis (still keeps the format)
    for row in mapp:
        emoji_row = [emojis.get(tile, tile) for tile in row]
        print("".join(emoji_row))

def finding_L(tups): # current location ni user
    r = len(tups)
    c = len(tups[0]) if r else 0
    grid = [list(row) for row in tups]
    for i in range(r):
        for j in range(c):
            if grid[i][j] == "L":
                return (i, j)

def mushroom_counter(tups):
    r = len(tups)
    c = len(tups[0]) if r else 0
    grid = [list(row) for row in tups]
    total_mushrooms = 0
    for i in range(r):
        for j in range(c):
            if grid[i][j] == "+":
                total_mushrooms += 1
    return total_mushrooms

def burn_trees(grid, x, y):
    if not (0 <= x < len(grid) and 0 <= y < len(grid[0])):
        return
    if grid[x][y] != "T":
        return
    grid[x][y] = "." # burned trees turns to empty
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
        burn_trees(grid, x + dx, y + dy)

def implement_game(filename):
    directions = {
    "W": (-1, 0),
    "A": (0, -1),
    "S": (1, 0),
    "D": (0, 1)
    }

    # initial load
    original_lines = load_mapp(filename)
    grid = load_grid_from_mapp(original_lines)
    player_loc = finding_L(original_lines)
    if player_loc is None:
        raise RuntimeError("No player 'L' found in the map file.")
    previous_tile = "."
    held_item = None
    total_mushrooms = mushroom_counter(original_lines)
    collected_mushrooms = 0
    number_of_undos = 3
    # previous state after a move has been done
    prev_state = {
        "grid": copy.deepcopy(grid),
        "player_loc": player_loc ,
        "previous_tile": previous_tile,
        "held_item": held_item,
        "collected_mushrooms": collected_mushrooms,
    }

    # main loop
    while True:
        clear()
        load_mapp_to_screen(["".join(row) for row in grid]) # starting map

        tile_under_name = tiles.get(previous_tile, "something mysterious")
        print()
        print(f"You are standing on: {tile_under_name}")
        print(f"Inventory: {tiles.get(held_item, held_item)}")
        print(f"You've collected {collected_mushrooms} out of {total_mushrooms} mushroom(s)")
        print()
        print("[W] - Move up")
        print("[A] - Move left")
        print("[S] - Move down")
        print("[D] - Move right")
        print("[P] - Pick up the item")
        print(f"[!] - Undo [{number_of_undos}] time(s)")
        print("[Q] - Leave the Game")
        print()
        # Win Conditions
        if total_mushrooms > 0 and collected_mushrooms == total_mushrooms:
            print("🎊 YOU WIN! 🎊")
            print(f"You collected all {total_mushrooms} mushrooms! 🍄🏆")
            input("Press Enter to exit...")
            break
        # movement
        move = input("What is your next move?: ").upper().strip()
        # ADHD entering
        if not move:
            continue
        # Quitting the Game
        if move == "Q":
            really = input("Are you sure? Y/N").upper().strip()
            if really == "Y":
                break
            else:
                continue
        # Undo
        if move == "!":
            if number_of_undos <= 0:
                print("🚫 You don't have any undos left buddy 🥀🥀")
                input("Press Enter to continue...")
                continue
            number_of_undos -= 1
            grid = copy.deepcopy(prev_state["grid"])
            player_loc = prev_state["player_loc"]
            previous_tile = prev_state["previous_tile"]
            held_item = prev_state["held_item"]
            collected_mushrooms = prev_state["collected_mushrooms"]
            print("↩️  Undo: reverted to previous move.")
            print(f"You only have {number_of_undos} undos left!")
            input("Press Enter to continue...")
            continue

        # Handling Items
        if move == "P":
            if previous_tile in ("x", "*"):
                if held_item:
                    print("You already have an item! Use it before picking up another.")
                    print("Press Enter to continue...")
                else:
                    held_item = previous_tile # 'x' or '*'
                    previous_tile = "."
                    print(f"You picked up {tiles[held_item]}!")
                    input("Press Enter to continue...")
            else:
                print("There is nothing to pick up here.")
                input("Press Enter to continue...")
            continue

        # Movement
        if move not in directions:
            print("Invalid move! Use W/A/S/D/P/!/Q")
            input("Press Enter to continue...")
            continue

        i, j = directions[move]
        x, y = player_loc
        new_x, new_y = x + i, y + j

        # Bounds check (stay inside map)
        if not (0 <= new_x < len(grid) and 0 <= new_y < len(grid[0])):
            print("🚫 You can't move beyond the edge of the map!")
            input("Press Enter to continue...")
            continue

        target = grid[new_x][new_y]

        # Save current state before making a move for the UNDO
        prev_state = {
            "grid": copy.deepcopy(grid),
            "player_loc": player_loc,
            "previous_tile": previous_tile,
            "held_item": held_item,
            "collected_mushrooms": collected_mushrooms,
        }

        # Rock pushing
        if target == "R":
            rock_x, rock_y = new_x + i, new_y + j
            # if within bounds
            if 0 <= rock_x < len(grid) and 0 <= rock_y < len(grid[0]):
                next_tile = grid[rock_x][rock_y]
                # pushes to empty
                if next_tile == ".":
                    grid[rock_x][rock_y] = "R" # Move the rock in the same direction as the player
                    grid[new_x][new_y] = "L" # Player takes over the rock's spot
                    grid[x][y] = previous_tile
                    previous_tile = "."
                    player_loc = (new_x, new_y)
                    continue
                elif next_tile == "~":
                    grid[rock_x][rock_y] = "_" # Move the rock into the water making a paved tile
                    grid[new_x][new_y] = "L" # Player takes over the rock's spot
                    grid[x][y] = previous_tile
                    previous_tile = "."
                    player_loc = (new_x, new_y)
                    print("💧 The rock sank and formed a path!")
                    input("Press Enter to continue...")
                    continue
                else:
                    continue # can't push onto non-empty non-water
            else:
                continue # rock would be out of bounds -> blocked


        # Drowning
        if target == "~":
            clear()
            load_mapp_to_screen(["".join(row) for row in grid])
            print()
            print("💦 You stepped into the water and drowned!")
            print("💀 GAME OVER ")
            ask = input("Would you still like to play the game? Y/N: ").upper().strip()
            if ask == "Y":
                if number_of_undos <= 0:
                    print("🚫 You don't have any undos left buddy 🥀🥀")
                    input("Press Enter to continue...")
                    break 
                number_of_undos -= 1
                grid = copy.deepcopy(prev_state["grid"])
                player_loc = prev_state["player_loc"]
                previous_tile = prev_state["previous_tile"]
                held_item = prev_state["held_item"]
                collected_mushrooms = prev_state["collected_mushrooms"]
                print("↩️  Undo: reverted to previous move.")
                print(f"You only have {number_of_undos} undos left!")
                input("Press Enter to continue...")
                continue
            else:
                print("Respect !!")
                break

        # Automatic tool use when moving into a tree
        if target == "T":
            if held_item == "x":
                print("🪓 You chopped down a tree!")
                grid[new_x][new_y] = "."
                held_item = None  # consumed
                input("Press Enter to continue...")
            elif held_item == "*":
                print("🔥 You unleashed the flamethrower!")
                burn_trees(grid, new_x, new_y)
                held_item = None  # consumed
                input("Press Enter to continue...")
            else:
                continue # no tool

        # Normal move
        grid[x][y] = previous_tile
        previous_tile = grid[new_x][new_y]
        grid[new_x][new_y] = "L"
        player_loc = (new_x, new_y)

        # Mushroom collection > 1
        if previous_tile == "+":
            collected_mushrooms += 1
            previous_tile = "." # mushroom removed
            print(f"🍄 You collected a mushroom! ({collected_mushrooms}/{total_mushrooms})")
            input("Press Enter to continue...")

if __name__ == "__main__":
    implement_game("testmap.txt")
