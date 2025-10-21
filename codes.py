TILE_EMOJIS = {
    "T": "🌲",  # tree
    ".": "  ",  # empty tile
    "+": "🍄",  # mushroom
    "R": "🪨",  # rock
    "~": "💧",  # water
    "-": "⬛",  # paved
    "x": "🪓",  # axe
    "*": "🔥",  # flamethrower
    "L": "🧑",  # Laro Craft (player)
}

def finding_L(tups):
    r = len(tups)
    c = len(tups[0]) if r else 0
    grid = [list(row) for row in tups]
    directions = [(1,0), (-1,0)]

    for i in range(r):
        for j in range(c):
            if grid[i][j] == "L":
                return (i, j)

def mapp(filename):
    with open(filename) as f:
        data = f.read().splitlines()
    return finding_L(data)
    # # return finding_L(data)
    #     emoji_lines = []
    #     for row in data:
    #         emoji_row = [TILE_EMOJIS.get(tile, tile) for tile in row]
    #         emoji_lines.append("".join(emoji_row))
    # return "\n".join(emoji_lines)

# def hanapin_si_L:

# def load_mapp(mapp):
#     for row in mapp:
#         emoji_row = [TILE_EMOJIS.get(tile, tile) for tile in row]
#         print("".join(emoji_row))
#         print()

print(mapp("testmap.txt"))
