import os

TILE_EMOJIS = {
    "T": "🌲",  # tree
    ".": "  ",  # empty tile
    "+": "🍄",  # mushroom
    "R": "🪨",  # rock
    "~": "🟦",  # water
    "_": "🟥",  # paved
    "x": "🪓",  # axe
    "*": "🔥",  # flamethrower
    "L": "🧑",  # Laro Craft (player)
}
# Displaying the map as emojis
def load_mapp(mapp): 
    emoji_rows = []
    for row in mapp:
        emoji_row = [TILE_EMOJIS[tile] if tile in TILE_EMOJIS else str(tile) for tile in row]
        emoji_rows.append("".join(emoji_row))
    
    result = "\n".join(emoji_rows)
    print(result)
    return result
    
# Clearing the terminal before displaying every output
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


