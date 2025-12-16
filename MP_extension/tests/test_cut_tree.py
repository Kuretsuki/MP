import pytest
from items_functionality import cut_tree

@pytest.mark.parametrize("grid_list, i, j, expected",[

# Tests for cases in which grid_list[i][j] is a tree
    ([".T.", "..T", ".T."], 2, 1, [".T.", "..T", "..."]),

    ([".T.", "._T", "TT."], 2, 1, [".T.", "._T", "T.."]),

    ([".T.", "TTT", ".T."], 1, 1, [".T.", "T.T", ".T."]),

    (["..T", ".++", ".T."], 0, 2, ["...", ".++", ".T."]),

    ([
         "TTTTTTTTT",
         "T...+..+T",
         "T+..~...T",
         "T...R.T.T",
         "T.T..TT.T",
         "T.x...*.T",
         "T.......T",
         "T.......T",
         "TTTTTTTTT"
     ], 4, 5, 

     [
         "TTTTTTTTT",
         "T...+..+T",
         "T+..~...T",
         "T...R.T.T",
         "T.T...T.T",
         "T.x...*.T",
         "T.......T",
         "T.......T",
         "TTTTTTTTT",
    ]),

    ([
         "TTTTTTTTT",
         "T...+..+T",
         "T+..~...T",
         "T...R.T.T",
         "T.T..TT.T",
         "T.x...*.T",
         "T.......T",
         "T.......T",
         "TTTTTTTTT"
     ], 0, 1, 
     [
         "T.TTTTTTT",
         "T...+..+T",
         "T+..~...T",
         "T...R.T.T",
         "T.T..TT.T",
         "T.x...*.T",
         "T.......T",
         "T.......T",
         "TTTTTTTTT"
     ]), 
    
    ([
         "TTTTTTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",

     ], 3, 4, 
     [
         "TTTTTTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
         "TTTT.TTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
     ]) ,
    

# Tests for cases in which grid_list[i][j] is a tree

    # grid_list[i][j] is a flamethrower
    ([".T.", "..T", ".*."], 2, 1, [".T.", "..T", ".*."]),

    # grid_list[i][j] is an axe
    ([".T.", "x.T", ".T."], 1, 0, [".T.", "x.T", ".T."]),

    # grid_list[i][j] is an empty tile
    (["...", "...", "..."], 1, 1, ["...", "...", "..."]),

    # grid_list[i][j] is rock
    ([".R.", "TRT", ".R."], 1, 1, [".R.", "TRT", ".R."]),

    # grid_list[i][j] is an axe
    ([".x.", "TxT", ".x."], 1, 1, [".x.", "TxT", ".x."]),

    # grid_list[i][j] is water
    ([
         "TTTTTTTTT",
         "T...+..+T",
         "T+..~...T",
         "T...R.T.T",
         "T.T..~T.T",
         "T.x...*.T",
         "T.......T",
         "T.......T",
         "TTTTTTTTT"
     ], 4, 5, 
     [
         "TTTTTTTTT",
         "T...+..+T",
         "T+..~...T",
         "T...R.T.T",
         "T.T..~T.T",
         "T.x...*.T",
         "T.......T",
         "T.......T",
         "TTTTTTTTT",
    ]),

    # grid_list[i][j] is a mushroom
    ([
         "+.TTTTTTT",
         "....+..+T",
         "T+..~...T",
         "T...R.T.T",
         "T.T..TT.T",
         "T.x...*.T",
         "T.......T",
         "T.......T",
         "TTTTTTTTT"
     ], 0, 0, 
     [
         "+.TTTTTTT",
         "....+..+T",
         "T+..~...T",
         "T...R.T.T",
         "T.T..TT.T",
         "T.x...*.T",
         "T.......T",
         "T.......T",
         "TTTTTTTTT"
    ]),

    # grid_list[i][j] is a paved tile
    ([
         "T_..TTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
     ], 0, 1, 
     [
         "T_..TTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
         "TTTTTTTTT",
    ])
    
])

def test_cut_tree(grid_list, i, j, expected):
    updatable_grid = [list(row) for row in grid_list]
    result = ["".join(row) for row in cut_tree(updatable_grid, i, j)]
    assert result == expected