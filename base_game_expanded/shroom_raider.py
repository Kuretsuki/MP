from argparse import ArgumentParser
from user_interaction import implement_game
import os
import time

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

def main():
    parser = ArgumentParser(description="Play Shroom Raider!")
    parser.add_argument("-f", "--stage_file", default="testmap.txt", help="Path to the stage file")
    parser.add_argument("-m", "--moves", default=None, help="String of moves to simulate (e.g., WASDP!Q)")
    parser.add_argument("-o", "--output", default=None, help="Output file for final map state")
    args = parser.parse_args()

    # AUTOMATED MODE
    if args.moves:
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
