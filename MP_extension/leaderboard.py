import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu(): 
    print("""
   _____ _                                _____       _     _   
  / ____| |                              |  __ \     (_)   | |
 | (___ | |__ _ ___  ___   __   _    _   | |__) |__ _ _  __| | ___ _ __
  \___ \| '_ \ ` _ \/ _ \ / _ \| \  / |  |  _  // _` | |/ _` |/ _ \ `__|
  ____) | | | | |  | (_) | (_) | |\/| |  | | \ \ (_| | | (_| |  __/ |
 |_____/|_| |_|_|   \___/ \___/|_|  |_|  |_|  \_\__,_|_|\__,_|\___|_|


        """)
    print("Press 1 to Play Game")
    print("Press 2 to View Leaderboard")
    print("Press 3 to Exit")
    return input("Choose an option: ")

def player_setup():
    while True:
        name = input("Enter your username: ").strip()
        if name:
            return name
        else:
            clear()
            print("Username cannot be empty! Please enter a name.")

def map_selector():
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
    map_filename = os.path.basename(map_file)
    with open("leaderboard.txt", "a") as f:
        f.write(f"{map_filename},{name},{time_taken}\n")

def load_leaderboard(map_file):
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
