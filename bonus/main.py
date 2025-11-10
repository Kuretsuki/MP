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
