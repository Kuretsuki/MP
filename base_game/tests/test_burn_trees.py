import pytest
from items_functionality import burn_trees

@pytest.mark.parametrize("grid_list, i, j, expected",[
    ([".T.", "..T", ".T."], 2, 1, [".T.", "..T", "..."]),
    ([".T.", "..T", ".T."], 1, 1, [".T.", "..T", ".T."]),
    ([
         "TTTTTTTTT",
         "T...+..+T",
         "T+..~...T",
         "T...R.T.T",
         "T.T.LTT.T",
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
         "T.T.L...T",
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
         "T.T.LTT.T",
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
         "..T.LTT..",
         "..x...*..",
         ".........",
         ".........",
         ".........",
    ])

])

def test_burn_trees(grid_list, i, j, expected):
    updatable_grid = [list(row) for row in grid_list]
    result = ["".join(row) for row in burn_trees(updatable_grid, i, j)]
    assert result == expected