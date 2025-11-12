from argparse import ArgumentParser
from user_interaction import implement_game

def main():
    parser = ArgumentParser(description="Play Shroom Raider!")
    parser.add_argument(
        "-f",
        "--stage_file",
        default="testmap.txt",
        help="Path to the stage file (e.g., testmap.txt)",
    )
    parser.add_argument(
        "-m", 
        "--moves", 
        default=None, 
        help="String of moves to simulate (e.g., WASDP!Q)")
    parser.add_argument(
        "-o", "--output", 
        default=None, 
        help="Output file for final map state")
    args = parser.parse_args()
    if args.moves:
        result = implement_game(args.stage_file, moves = args.moves, output_file = args.output)
        while result == "RESET":
            result = implement_game(args.stage_file, moves=args.moves, output_file=args.output)
        return

    while True:
        result = implement_game(args.stage_file)
        while result == "RESET":
            result = implement_game(args.stage_file)
        if result in ("CLEAR", "NO CLEAR", True, False):
            break


if __name__ == "__main__":
    main()

