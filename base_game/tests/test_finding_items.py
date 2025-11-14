import pytest
from map_tracking import finding_items

@pytest.mark.parametrize("grid_list, expected", [
# Note: expected = [[location of axe/s], [location of flamethrower/s]]

# Suppose the text file containing the map was empty
    ([], ([], [])),


# For simply checking functionality

     # No item is available
    (["..."], ([], [])),

    # Both axe/s and flamethrower/s is/are available
    (["*x"], ([(0,1)], [(0,0)])),

    (["x..", ".*."], ([(0,0)], [(1,1)])),

    # Only flamethrower/s is/are available
    ([".L.", "***"], ([], [(1,0), (1,1), (1,2)])),

    # Only flamethrower/s is/are available
    (["xxx", "..L"], ([(0,0), (0,1), (0,2)], [])),



# Test for the actual map used as default
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
     ], ([(5,2)], [(5,6)])),


# Tests for other forms of map
    ([
         "TTTTTTTTTTT",
         "T...+..+.xT",
         "T+..~.....T",
         "T...R*T...T",
         "T.T.LTT...T",
         "T.x...*...T",
         "T.........T",
         "T.*......xT",
         "TTTTTTTTTTT"
     ], ([(1,9), (5,2), (7,9)], [(3,5), (5,6), (7,2)])),

    ([
         "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
         "T...+..+.xx..............**..T",
         "T+..~........................T",
         "T...R*T......................T",
         "T.T.LTT......................T",
         "T.x...*......................T",
         "T............................T",
         "T.****.................xxxxxxT",
         "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",

     ], ([(1,9), (1,10), (5,2), (7,23), (7, 24), (7,25), (7,26), (7,27), (7,28)], [(1,25), (1,26), (3,5), (5,6), (7,2), (7,3), (7,4), (7,5)])),


    ([
         "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
         "T...+..+.xx..............**..T",
         "T+..~........................T",
         "T...R*T......................T",
         "T.T.LTT......................T",
         "T.x...*......................T",
         "T............................T",
         "T.****.................xxxxxxT",
         "T.****.................xxxxxxT",
         "T.****.................xxxxxxT",
         "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",

     ], (
          [(1,9), (1,10), (5,2), (7,23), (7,24), (7,25), (7,26), (7,27), (7,28), (8,23), (8,24), (8,25), (8,26), (8,27), (8,28), (9,23), (9, 24), (9,25), (9,26), (9,27), (9,28)], 
          [(1,25), (1,26), (3,5), (5,6), (7,2), (7,3), (7,4), (7,5), (8,2), (8,3), (8,4), (8,5), (9,2), (9,3), (9,4), (9,5)])
     )
])
def test_finding_items(grid_list, expected):
    assert finding_items(grid_list) == expected

