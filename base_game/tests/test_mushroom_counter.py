import pytest
from map_tracking import mushroom_counter

@pytest.mark.parametrize("grid_list, expected", [
    ([], 0),
    (["..."], 0),
    ([""], 0),
    (["+"], 1),
    (["*x+"], 1),
    (["+++", ".*+"], 4),
    (["..+", "L++"], 3),
    ([".L.", "***", "+++"], 3),
    ([
         "TTTTTTTTT",
         "T...+..+T",
         "T+..~...T",
         "T...R.T.T",
         "T.T.LTT.T",
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
         "T.T.LTT...T",
         "T.x...*++.T",
         "T.........T",
         "T.*......xT",
         "TTTTTT++TTT"
     ], 7)

])

def test_mushroom_counter(grid_list, expected):
    assert mushroom_counter(grid_list) == expected