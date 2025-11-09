from argparse import ArgumentParser
from user_interaction import implement_game

if __name__ == "__main__":
    parser = ArgumentParser(description="Play Shroom Raider!")
    parser.add_argument(
        "stage_file",
        nargs="?",
        default="testmap.txt",
        help="Path to the stage file (e.g., testmap.txt)",
    )
    args = parser.parse_args()
    implement_game(args.stage_file)
