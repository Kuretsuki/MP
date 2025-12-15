def burn_trees(grid, x, y):
    """
    Activates the flamethrower functionality to burn trees.

    Args:
        grid (list): The current game map grid
        x (int): The x coordinate of the tree that will be burned
        y (int): The y coordinate of the tree that will be burned

    Process:
        The function loops through all the trees that is found in
        orthogonal direction until it cannot find one.

    Returns:
        list: The updated grid with burned trees removed
    """
    if not (0 <= x < len(grid) and 0 <= y < len(grid[x])):
        return grid
    if grid[x][y] != "T":
        return grid
    grid[x][y] = "." # burned trees turns to empty
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        burn_trees(grid, x + dx, y + dy)
    return grid


# Axe functionality
def cut_tree(grid, x, y):
     """
    Activates the axe functionality to cut trees.

    Args:
        grid (list): The current game map grid
        x (int): The x coordinate of the tree that will be cut
        y (int): The y coordinate of the tree that will be cut

    Process:
        Assigns the grid[x][y] to be a "." which makes that element
        of the grid to be walkable.

    Returns:
        list: The updated grid with the removed tree.
    """
    if grid[x][y] == "T":
        grid[x][y] = "."
    return grid


