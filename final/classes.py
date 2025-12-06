from dataclasses import dataclass

class GameMap:
    grid: list
    axes_loc: set
    fires_loc: set
    rock_underlying_tiles: dict

    def in_bounds(self, x, y):
        return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[x])

    def get(self, x, y):
        return self.grid[x][y]

    def set(self, x, y, value):
        self.grid[x][y] = value

class Player:
    x: int
    y: int
    held_item: str
    collected_mushroom: int
    previous_loc: str

    
