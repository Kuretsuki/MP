from new_user_interaction import implement_game
from leaderboard import main_menu, player_setup, save_score, show_leaderboard, map_selector
import os
import time

def clear():
    """
    Clears the console screen based on the operating system.
    
    Uses 'cls' for Windows (nt) and 'clear' for Unix/Linux systems.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """
    The main entry point for the Shroom Raider game.

    This function runs the primary application loop, handling:
    1. Displaying the main menu.
    2. Player setup and map selection.
    3. Initiating the game loop and tracking play duration.
    4. Handling game results (Win/Reset/Quit) and saving high scores.
    5. Displaying the leaderboard for specific maps.
    
    The loop continues until the user selects option '3' to exit.
    """
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
