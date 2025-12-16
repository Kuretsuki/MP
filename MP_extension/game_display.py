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

def load_mapp(mapp): 
    """
    Gets the copy of the grid that is in text form and converts it to emojis.

    Args:
        mapp (list[str]): The map that is in text form, i.e ["TT.LT", "....."]

    Returns:
        A map in emoji form, that is seperated by a newline in every rows.
    """
    emoji_rows = []
    for row in mapp:
        emoji_row = [TILE_EMOJIS[tile] if tile in TILE_EMOJIS else str(tile) for tile in row]
        emoji_rows.append("".join(emoji_row))
    
    result = "\n".join(emoji_rows)
    print(result)
    return result
    
def clear():
    # Clearing the terminal before displaying every output
    os.system('cls' if os.name == 'nt' else 'clear')





