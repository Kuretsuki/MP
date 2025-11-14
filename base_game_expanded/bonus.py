def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

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
