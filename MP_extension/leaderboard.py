import os

def clear():
    """
    Clears the console screen based on the operating system.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu(): 
    """
    Displays the main game menu and prompts the user for a selection.

    Prints the game title ASCII art and the available options:
    1. Play Game
    2. View Leaderboard
    3. Exit

    Returns:
        str: The option selected by the user (e.g., "1", "2", "3").
    """
    print(r"""
    _____ _                               _____       _     _    
   / ____| |                             |  __ \     (_)   | |   
  | (___ | |__ _ ___  ___  __  _     _   | |__) |__ _ _  __| | ___ _ __ 
   \___ \| '_ \ ` _ \/ _ \ / _ \| \  / | |  _  // _` | |/ _` |/ _ \ `__|
   ____) | | | | |  | (_) | (_) | |\/| | | | \ \ (_| | | (_| |  __/ |   
  |_____/|_| |_|_|   \___/ \___/|_|  |_| |_|  \_\__,_|_|\__,_|\___|_|   


        """)
    print("Press 1 to Play Game")
    print("Press 2 to View Leaderboard")
    print("Press 3 to Exit")
    return input("Choose an option: ")

def player_setup():
    """
    Prompts the player to enter a non-empty username.

    Loop continues until a valid name is provided.

    Returns:
        str: The validated username entered by the player.
    """
    while True:
        name = input("Enter your username: ").strip()
        if name:
            return name
        else:
            clear()
            print("Username cannot be empty! Please enter a name.")

def map_selector():
    """
    Lists available map files in the 'maps' directory and handles user selection.

    Scans the 'maps' folder for .txt files. If no maps or directory are found,
    defaults to 'testmap.txt'.

    Returns:
        str: The relative path to the selected map file (e.g., 'maps/level1.txt').
    """
    clear()
    print("=== MAP SELECTOR ===")
    
    if not os.path.exists("maps"):
        print("Maps directory not found! Using default: testmap.txt")
        return "testmap.txt"
    
    map_files = sorted([f for f in os.listdir('maps') if f.endswith('.txt')])
    
    if not map_files:
        print("No map files found! Using default: testmap.txt")
        return "testmap.txt"
    
    print("Available Maps:")
    for i, map_file in enumerate(map_files, 1):
        map_name = map_file.replace('.txt', '').replace('_', ' ').title()
        print(f"{i}. {map_name}")
    
    while True:
        try:
            choice = input(f"\nSelect a map (1-{len(map_files)}): ").strip()
            
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(map_files):
                    selected_map = map_files[choice_num - 1]
                    return os.path.join("maps", selected_map)
                else:
                    print(f"Please enter a number between 1 and {len(map_files)}")
                    input("Press any key to continue...")
                    clear()
                    print("=== MAP SELECTOR ===")
                    print("Available Maps:")
                    for i, map_file in enumerate(map_files, 1):
                        map_name = map_file.replace('.txt', '').replace('_', ' ').title()
                        print(f"{i}. {map_name}")
            else:
                print("Please enter a valid number")
                input("Press any key to continue...")
                clear() 
                print("=== MAP SELECTOR ===")
                print("Available Maps:")
                for i, map_file in enumerate(map_files, 1):
                    map_name = map_file.replace('.txt', '').replace('_', ' ').title()
                    print(f"{i}. {map_name}")
                
        except (ValueError, IndexError):
            print("Invalid selection!")
            input("Press any key to continue...")
            clear()
            print("=== MAP SELECTOR ===")
            print("Available Maps:")
            for i, map_file in enumerate(map_files, 1):
                map_name = map_file.replace('.txt', '').replace('_', ' ').title()
                print(f"{i}. {map_name}")


def save_score(name, time_taken, map_file):
    """
    Appends a player's score to the 'leaderboard.txt' file.

    Args:
        name (str): The player's username.
        time_taken (float): The time elapsed to complete the level.
        map_file (str): The path or name of the map played.
    """
    map_filename = os.path.basename(map_file)
    with open("leaderboard.txt", "a") as f:
        f.write(f"{map_filename},{name},{time_taken}\n")

def load_leaderboard(map_file):
    """
    Loads and sorts scores for a specific map from 'leaderboard.txt'.

    Reads the leaderboard file, filters entries matching the provided map name,
    and sorts them by time taken (ascending).

    Args:
        map_file (str): The path or name of the map to load scores for.

    Returns:
        list[tuple]: A list of tuples where each tuple contains (name, time_taken).
        The list is sorted with the fastest times first.
    """
    scores = []
    map_filename = os.path.basename(map_file)
    if os.path.exists("leaderboard.txt"):
        with open("leaderboard.txt") as f:
            for line in f:
                entry_map, name, time_taken = line.strip().split(",")
                if entry_map == map_filename:
                    scores.append((name, float(time_taken)))
    def get_time(score_tuple):
        return score_tuple[1]
        
    scores.sort(key=get_time)
    return scores

def show_leaderboard(map_file):
    """
    Displays the top 10 scores for the selected map and handles clearing options.

    Prints the leaderboard to the console. Also provides an option for the user
    to clear the leaderboard for the current map.

    Args:
        map_file (str): The path or name of the map to display scores for.
    """
    clear()
    map_filename = os.path.basename(map_file)
    scores = load_leaderboard(map_file)
    print(f"=== LEADERBOARDS: {map_filename} ===")
    if not scores:
        print("No records yet!")
    else:
        for i, (name, t) in enumerate(scores[:10], start=1):
            print(f"{i}. {name} - {t:.2f} seconds")

    print("\nOptions:")
    print("[C] Clear Leaderboards for THIS MAP")
    print("[Enter] Return to Menu")
    
    choice = input("Choose an option: ").strip().upper()

    if choice == "C":
        clear_current_map_leaderboard(map_file)
        print(f"Leaderboard for {map_filename} has been cleared!")
        input("Press any key to continue...")

def clear_current_map_leaderboard(map_file):
    """
    Removes all scores associated with a specific map from 'leaderboard.txt'.

    Reads all records, filters out those belonging to the specified map,
    and rewrites the file with the remaining records.

    Args:
        map_file (str): The path or name of the map to clear scores for.
    """
    map_filename = os.path.basename(map_file)
    
    if not os.path.exists("leaderboard.txt"):
        return

    kept_records = []
    with open("leaderboard.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entry_map, name, time_taken = line.split(",")
                    if entry_map != map_filename:
                        kept_records.append(line)
                except ValueError:
                    continue
    
    # Write back only the kept records
    with open("leaderboard.txt", "w") as f:
        for record in kept_records:
            f.write(record + "\n")
