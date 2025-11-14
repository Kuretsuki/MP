import pytest
from map_tracking import mushroom_counter

@pytest.mark.parametrize("grid_list, expected", [
# Tests for checking functionality
    ([], 0),

    (["...", "...", "..."], 0),

    (["...", ".~.", "_TT"], 0),

    (["+++", ".*+", "..."], 4),

    (["..+", ".++", "_.."], 3),

    ([".L.", "***", "+++"], 3),

# Test for the actual map used as default
    ([
         "TTTTTTTTT",
         "T...+...T",
         "T...~...T",
         "T...R.T.T",
         "T.T..TT.T",
         "T.x...*.T",
         "T.......T",
         "T.......T",
         "TTTTTTTTT"
     ], 1),


# Other tests
    ([
         "TTTTTTTTT",
         "T...+..+T",
         "T+..~...T",
         "T...R.T.T",
         "T.T..TT.T",
         "T.x...*.T",
         "T.......T",
         "T++.....T",
         "TTTTTTTTT"
     ], 5),


    ([
         "TTTTTTTTT",
         "T...+..+T",
         "T+..~...T",
         "T...R.T.T",
         "T.T..TT.T",
         "T.x...*.T",
         "T.......T",
         "T++.....T",
         "TTTTTTTTT"
     ], 5),
    ([
         "TTTTTTTTTTT",
         "T...+..+.xT",
         "T+..~.....T",
         "T...R*T...T",
         "T.T..TT...T",
         "T.x...*++.T",
         "T.........T",
         "T.*......xT",
         "TTTTTT++TTT"
     ], 7),

        ([
         "+++++++++++",
         "+++++++++++",
         "+++++++++++",
         "+++++++++++",
         "+++++++++++",
         "+++++++++++",
         "+++++++++++",
         "+++++++++++",
         "+++++++++++"
     ], 99),

        ([
         "++++++++++++++++++++",
         "+..................+",
         "+..................+",
         "+..................+",
         "+..................+",
         "+..................+",
         "+..................+",
         "+..................+",
         "++++++++++++++++++++"
     ], 54)

])

def test_mushroom_counter(grid_list, expected):
    assert mushroom_counter(grid_list) == expected