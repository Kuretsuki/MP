from new_user_interaction import implement_game
from leaderboard import main_menu, player_setup, save_score, load_leaderboard, show_leaderboard, map_selector
import os
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        clear()
        choice = main_menu()
        if choice == "1":
            clear()
            name = player_setup()
            selected_map = map_selector()
            
            input(f"\n{name}, get ready to become a Shroom Raider!\nMap: {os.path.basename(selected_map)}\nPress any key to start the game...")
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
            input("\nPress any key to return to menu...")
        elif choice == "2":
            map_for_leaderboard = map_selector()
            show_leaderboard(map_for_leaderboard)
        elif choice == "3":
            print("I am sure you'll be back...")
            break
        else:
            print("Invalid choice! Use 1/2/3.")
            input("Press any key to continue...")


if __name__ == "__main__":
    main()
