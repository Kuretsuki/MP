from argparse import ArgumentParser
from user_interaction import implement_game
from bonus import main_menu, player_setup, save_score, load_leaderboard, show_leaderboard, map_selector
import os
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def resolve_map_path(map_file):
    if os.path.exists(map_file):
        return map_file
    
    maps_path = os.path.join("maps", map_file)
    if os.path.exists(maps_path):
        return maps_path
    
    map_filename = os.path.basename(map_file)
    maps_path = os.path.join("maps", map_filename)
    if os.path.exists(maps_path):
        return maps_path
    
    return map_file

def main():
    parser = ArgumentParser(description="Play Shroom Raider!")
    parser.add_argument("-f", "--stage_file", default="testmap.txt", help="Path to the stage file (will check in 'maps' directory)")
    parser.add_argument("-m", "--moves", default=None, help="String of moves to simulate (e.g., WASDP!Q)")
    parser.add_argument("-o", "--output", default=None, help="Output file for final map state")
    args = parser.parse_args()

    resolved_stage_file = resolve_map_path(args.stage_file)
    
    # AUTOMATED MODE (uses command line stage_file)
    if args.moves:
        result = implement_game(resolved_stage_file, moves=args.moves, output_file=args.output, silent=True)
        return
        
    # INTERACTIVE MODE 
    while True:
        clear()
        choice = main_menu()
        if choice == "1":
            clear()
            name = player_setup()
            selected_map = map_selector()
            
            input(f"\n{name}, get ready to become a Shroom Raider!\nMap: {os.path.basename(selected_map)}\nPress Enter to start the game...")
            start = time.time()
            result = implement_game(selected_map)
            while result == "RESET":
                result = implement_game(selected_map)
            end = time.time()
            duration = end - start
            if result is True:
                print(f"\n{name}, you finished in {duration:.2f} seconds!")
                save_score(name, duration, selected_map)
            elif result == "QUIT":
                print("You Quit!")
            input("\nPress Enter to return to menu...")
        elif choice == "2":
            map_for_leaderboard = map_selector()
            show_leaderboard(map_for_leaderboard)
        elif choice == "3":
            print("I am sure you'll be back...")
            break
        else:
            print("Invalid choice! Use 1/2/3.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
