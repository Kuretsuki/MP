import os

# Accessing testmap.txt and turning it into a processable list of strings 
def mapp(filename): 
    if not os.path.exists(filename):
        print(f"Error: Map file '{filename}' not found!")
        exit(1)
    with open(filename, encoding = "utf=8") as f:
        data = f.read().splitlines()
    return data

# Tracking in which (i, j) in the map the user will start at
def finding_L(tups):
    r = len(tups)
    c = len(tups[0]) if r else 0
    grid = [list(row) for row in tups]
    directions = [(1,0), (-1,0)]

    for i in range(r):
        for j in range(c):
            if grid[i][j] == "L":
                return (i, j)
                
# Tracking in which (i, j)'s' in the map are the items located at
def finding_items(tups):
    r = len(tups)
    c = len(tups[0]) if r else 0
    grid = [list(row) for row in tups]
    directions = [(1,0), (-1,0)]
    axe = []
    fire = []

    for i in range(r):
        for j in range(c):
            if grid[i][j] == "x":
                axe.append((i, j))
            elif grid[i][j] == "*":
                fire.append((i ,j))
    return (axe, fire)

# Counting the total mushrooms in the map
def mushroom_counter(tups): 
    r = len(tups)
    c = len(tups[0]) if r else 0
    grid = [list(row) for row in tups]
    total_mushrooms = 0
    for i in range(r):
        for j in range(c):
            if grid[i][j] == "+":
                total_mushrooms += 1
    return total_mushrooms  
