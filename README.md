# Shroom Raider

## How to Run the Game
1. Download all files in the folder.  
2. Make sure all files are in the same folder or follow the directory structure.  
3. Open WSL (Windows Subsystem for Linux) or your preferred terminal.
(Note: It is advisable to use the latest version of Python to ensure compatibility with all dependencies.)
4. Install the required dependencies with:
   ```bash
   python3 -m pip install -r requirements.txt
6. Run the main program
   ```bash
   python3 main.py
7. The following are some other arguments that can be added at the end of the command:
   - " -f <map.txt>", to specify which map to play
   - The following are used in automated mode"
   - " -m <"www">, to give a specific string of moves (case-insensitive)
   - " -o <output.txt>", to specify which file would the result be sent at
8. Use the controls to play:
- W: Move up
- A: Move left
- S: Move down
- D: Move right
- P: Pick up item
- !: Reset
- Q: Quit

## Code Organization
1. `shroom_raider.py` - Entry point for the game. Handles starting the game and user input.
2. `game_display.py` - Functions related to displaying the map, clearing the screen, and tile emojis.
3. `items_functionality.py` - Functions to interact with items (cutting trees, burning trees, etc.).
4. `map_tracking.py` - Functions to track the map, player location, and mushrooms.
5. `user_interaction.py` - Function that handles user's interaction with the environment.
6. `game_main_controls.py` - Functions that processes the primary moves W, A, S, D, and P.
7. `bonus/` - Directory that contains all the bonus functions

## Algorithm Overview
- The game is a grid-based simulation.
- The player moves with W/A/S/D, interacts with items using P, and can reset with !.
- Movement checks for obstacles (trees, rocks, water) and handles item usage.
- The game ends if the player falls in water or collects all mushrooms.
- Each frame, the map is updated and displayed using load_mapp.

## Resources
1. [PyPI](https://pypi.org/project/termcolor/)
