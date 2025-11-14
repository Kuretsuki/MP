import pytest
from items_functionality import burn_trees

@pytest.mark.parametrize(
    "grid_list, i, j, expected",
    [
    # Tests for cases in which the grid_list[i][j] is actually a tree
        ([".T.", "..T", ".T."], 2, 1, [".T.", "..T", "..."]),

        ([".T.", ".TT", ".T."], 1, 1, ["...", "...", "..."]),

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
             "T...R...T",
             "T.T.....T",
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
         ], 0, 0, 
         [
             ".........",
             "....+..+.",
             ".+..~....",
             "....R.T..",
             "..T..TT..",
             "..x...*..",
             ".........",
             ".........",
             ".........",
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
         ], 0, 1, 
         [
             ".........",
             ".........",
             ".........",
             ".........",
             ".........",
             ".........",
             ".........",
             ".........",
        ]),

        # Test for non-adjacent trees
        ([   "T........",
             ".T.......",
             "..T......",
             "...T.....",
             "....T....",
             ".....T...",
             "......T..",
             ".......T.",
        ], 1, 1,
        [    "T........",
             ".........",
             "..T......",
             "...T.....",
             "....T....",
             ".....T...",
             "......T..",
             ".......T.",
        ]),

        # Test for adjacent trees together with non-adjacent trees
        ([
             "TTTTTTTTT",
             "T........",
             "TTTTTTTTT",
             "........T",
             "TTTTTTTTT",
             "T........",
             ".TTTTTTTT",
             "TTTTTTTTT",
         ], 0, 8, 
        [    ".........",
             ".........",
             ".........",
             ".........",
             ".........",
             ".........",
             ".TTTTTTTT",
             "TTTTTTTTT",
        ]),

       ([
             "TTTTTTTTTTTTTTT",
             "T.............T",
             "T...TTTTTTT...T",
             "T...T.....T...T",
             "T...TTTTTTT...T",
             "T.............T",
             "TTTTTTTTTTTTTTT",

         ], 2, 4, 
         [   "TTTTTTTTTTTTTTT",
             "T.............T",
             "T.............T",
             "T.............T",
             "T.............T",
             "T.............T",
             "TTTTTTTTTTTTTTT",
        ]),

        # Tests for adjacent trees
        ([
             "TTTTTTTTTTTTTTT",
             "T..............",
             "TTTTTTTTTTTTTTT",
             "..............T",
             "TTTTTTTTTTTTTTT",
             "T..............",
             "TTTTTTTTTTTTTTT",

         ], 0, 14, 
         [   "...............",
             "...............",
             "...............",
             "...............",
             "...............",
             "...............",
             "...............",
        ]),

        ([
             "TTTTTTTTTTTTTTT",
             "T.............T",
             "T...TTTTTTT...T",
             "T...T.....T...T",
             "T...T.....T...T",
             "T...T.....T...T",
             "TTTTTTTTTTTTTTT",

         ], 2, 4, 
         [   "...............",
             "...............",
             "...............",
             "...............",
             "...............",
             "...............",
             "...............",
        ]),

 

    # Tests for cases in which grid_list[i][j] is not a tree

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
    ]
)

def test_burn_trees(grid_list, i, j, expected):
    updatable_grid = [list(row) for row in grid_list]
    result = ["".join(row) for row in burn_trees(updatable_grid, i, j)]
    assert result == expected