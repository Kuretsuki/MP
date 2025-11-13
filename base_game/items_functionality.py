# Flame thrower functionality
def burn_trees(grid, x, y):
    if not (0 <= x < len(grid) and 0 <= y < len(grid[0])):
        return grid
    if grid[x][y] != "T":
        return grid
    grid[x][y] = "." # burned trees turns to empty
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        burn_trees(grid, x + dx, y + dy)
    return grid


# Axe functionality
def cut_tree(grid, x, y):
    if grid[x][y] == "T":
        grid[x][y] = "."
    return grid
