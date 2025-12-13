from dataclasses import dataclass
from termcolor import colored
from items_functionality import burn_trees, cut_tree
from game_display import clear, load_mapp
import os
import time

@dataclass
class Map:
    filename: str

    def get_map(self) -> list[list[str]]:
        if not os.path.exists(self.filename):
            raise ValueError(f"Error: Map file '{self.filename}' not found!")
        with open(self.filename, encoding = "utf-8") as f:
            data = f.read().splitlines()
            grid = [list(row) for row in data]
        return grid

class Locations:
    def __init__(self, filename):
        self.items_loc = ([],[])
        self.mushroom_count = 0
        self.player_loc = None
        self.playing_map = Map(filename).get_map()
        self.r = len(self.playing_map)
        self.c = len(self.playing_map[0])
        super().__init__()
        
    def find_L(self):
        for i in range(self.r):
            for j in range(len(self.playing_map[i])):
                if self.playing_map[i][j] == "L":
                    self.player_loc = (i, j)

    def find_items(self):
        for i in range(self.r):
            for j in range(len(self.playing_map[i])):
                if self.playing_map[i][j] == "x":
                    self.items_loc[0].append((i,j))

        for i in range(self.r):
            for j in range(len(self.playing_map[i])):
                if self.playing_map[i][j] == "*":
                    self.items_loc[1].append((i,j))

    def count_mushroom(self):
        for i in range(self.r):
            for j in range(len(self.playing_map[i])):
                if self.playing_map[i][j] == "+":
                    self.mushroom_count += 1

class Interactive:
    def __init__(self, filename):
        location = Locations(filename)
        location.find_L()
        location.find_items()
        location.count_mushroom()
        self.playing_map = location.playing_map
        self.player_loc = location.player_loc
        self.axes_loc, self.fires_loc = location.items_loc[0] , location.items_loc[1]
        self.mushroom_count = location.mushroom_count
        self.directions = {
        "W": (-1, 0),
        "A": (0, -1),
        "S": (1, 0),
        "D": (0, 1),
        "P": (0, 0),
        "!": (0, 0),
        "Q": (0, 0)
    }
        self.current_mushroom = 0
        self.pick_up_message = ""
        self.previous_loc = "."
        self.held_items = None
        self.rock_underlying_tiles = {}
        self.state = None

    def handle_movement(self, move, silent = False, delay = False, multi_move = False):
        x, y = self.player_loc
        i, j = self.directions[move.upper()]
        next_x, next_y = x + i, y + j
        delay = True

        # Checking if movement is within map bounds
        if not (0 <= next_x < len(self.playing_map) and 0 <= next_y < len(self.playing_map[next_x])):
            partial_res = ["".join(row) for row in self.playing_map]
            if silent is False:
                clear()
                load_mapp(partial_res)
                print(colored("\nYou cannot move outside the map!", "red"))
            return 

        target_cell = self.playing_map[next_x][next_y]

        # Moving on a valid tile
        if target_cell in [".", "_", "*", "x", "T"]:
            if target_cell == "T":  # Tree interaction
                if self.held_items == "x":
                    cut_tree(self.playing_map, next_x, next_y)
                    self.held_items = None
                    self.pick_up_message = colored("You used an axe!", "yellow")
                elif self.held_items == "*":
                    burn_trees(self.playing_map, next_x, next_y)
                    self.held_items = None
                    self.pick_up_message = colored("You used a flamethrower!", "yellow")
                else:
                    partial_res = ["".join(row) for row in self.playing_map]
                    if silent is False:
                        clear()
                        load_mapp(partial_res)
                        print(colored("\nThere's a tree blocking your path!", "red"))
                    return 

            self.playing_map[x][y] = self.previous_loc
            self.previous_loc = self.playing_map[next_x][next_y]
            self.playing_map[next_x][next_y] = "L"
            if silent is False:
                clear()
                load_mapp(["".join(row) for row in self.playing_map])

            if delay and multi_move:
                time.sleep(0.25)

            x, y = next_x, next_y
            self.player_loc = (x, y)
            # return (next_x, next_y), previous_loc, held_items, current_mush, None, pick_up_message, rock_underlying_tiles

        # Pushing rocks
        elif target_cell == "R":
            next_two_x, next_two_y = x + 2*i, y + 2*j
            if not (0 <= next_two_x < len(self.playing_map) and 0 <= next_two_y < len(self.playing_map[next_two_x])):
                partial_res = ["".join(row) for row in self.playing_map]
                if silent is False:
                    clear()
                    load_mapp(partial_res)
                    print(colored("\nYou can't push the rock off the map!", "red"))
                return 

            next_cell = self.playing_map[next_two_x][next_two_y]
            rock_pos = (next_x, next_y)

            if rock_pos in self.rock_underlying_tiles:
                tile_under_rock = self.rock_underlying_tiles[rock_pos]
                del self.rock_underlying_tiles[rock_pos]
            else:
                tile_under_rock = "."

            # If rock is pushed on an empty tile
            if next_cell == ".":
                self.playing_map[next_two_x][next_two_y] = "R"
                self.playing_map[next_x][next_y] = "L"
                self.playing_map[x][y] = self.previous_loc
                self.previous_loc = tile_under_rock
                self.rock_underlying_tiles[(next_two_x, next_two_y)] = "."
                self.player_loc = (next_x, next_y)

            # If rock is pushed in the water
            elif next_cell == "~":
                self.playing_map[next_two_x][next_two_y] = "_"
                self.playing_map[next_x][next_y] = "L"
                self.playing_map[x][y] = self.previous_loc
                self.previous_loc = tile_under_rock
                self.player_loc = (next_x, next_y)

            # If rock is pushed on a paved-tile
            elif next_cell == "_":
                self.playing_map[next_two_x][next_two_y] = "R"
                self.playing_map[next_x][next_y] = "L"
                self.playing_map[x][y] = self.previous_loc
                self.previous_loc = tile_under_rock  
                self.rock_underlying_tiles[(next_two_x, next_two_y)] = "_"
                self.player_loc = (next_x, next_y)

            # If rock is pushed on a tree or mushroom
            elif next_cell in ["T", "+"]:
                partial_res = ["".join(row) for row in self.playing_map]
                obstacle = "tree" if next_cell == "T" else "mushroom"
                if silent is False:
                    clear()
                    load_mapp(partial_res)
                    print(colored(f"\nThere's a {obstacle} blocking your path!", "red"))
                return 

            # If two or more rock is pushed 
            elif next_cell == "R":
                partial_res = ["".join(row) for row in self.playing_map]
                if silent is False:
                    clear()
                    load_mapp(partial_res)
                    print(colored("\nYou're not strong enough to push multiple rocks!", "red"))
                return 

            if silent is False:
                clear()
                load_mapp(["".join(row) for row in self.playing_map])
            if delay and multi_move:
                time.sleep(0.15)

            return 
            # return current_loc, previous_loc, held_items, current_mush, None, pick_up_message, rock_underlying_tiles

        # Collecting mushrooms
        elif target_cell == "+":
            self.current_mushroom += 1
            self.playing_map[x][y] = self.previous_loc
            self.previous_loc = "."
            self.playing_map[next_x][next_y] = "L"
            self.player_loc = (next_x, next_y)
            if silent is False:
                clear()
                load_mapp(["".join(row) for row in self.playing_map])

            # Collected all mushrooms - Winning state
            if self.current_mushroom == self.mushroom_count:
                if silent is False:
                    print(colored("\nCongratulations!", "yellow"))
                    print(f"\n{self.current_mushroom} out of {self.mushroom_count} mushroom(s) collected\n")
                self.state = True
                # return current_loc, previous_loc, held_items, current_mush, True, pick_up_message, rock_underlying_tiles

            return 
            # return current_loc, previous_loc, held_items, current_mush, None, pick_up_message, rock_underlying_tiles

        # Falling in the water - Losing State
        elif target_cell == "~":
            self.playing_map[x][y] = self.previous_loc
            self.player_loc = (next_x, next_y)
            if silent is False:
                clear()
                load_mapp(["".join(row) for row in self.playing_map])
                print(colored("\nGame Over!", "red"))
                print(colored("You fell in the water!"))
                print(f"\n{self.current_mushroom} out of {self.mushroom_count} mushroom(s) collected\n")

            self.state = False
            # return current_loc, previous_loc, held_items, current_mush, False, pick_up_message, rock_underlying_tiles


    def handle_pickup(self):
        x, y = self.player_loc
        if self.previous_loc in ["*", "x"] and not self.held_items:
        # Pick up available item
            if self.previous_loc == "x":
                if self.player_loc in self.axes_loc:
                    self.axes_loc.remove(self.player_loc)
                self.held_items = self.previous_loc
                self.pick_up_message = colored("You picked up an axe!", "yellow")
            else:
                if self.player_loc in self.fires_loc:
                    self.fires_loc.remove(self.player_loc)
                self.held_items = self.previous_loc
                self.pick_up_message = colored("You picked up a flamethrower!", "yellow")
            self.previous_loc = "."
        elif self.previous_loc not in ["*", "x"]:
            self.pick_up_message = colored("There is no item to be picked up!", "red")
        else:
            self.pick_up_message = colored("You are already holding an item!", "red")

        self.playing_map[x][y] = "L"
        return 








