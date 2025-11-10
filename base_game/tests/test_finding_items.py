import pytest
from map_tracking import finding_items

@pytest.mark.parametrize("grid_list, expected", [
    ([], ([], [])),
    (["..."], ([], [])),
    (["*x"], ([(0,1)], [(0,0)])),
    (["x..", ".*."], ([(0,0)], [(1,1)])),
    (["xxx", "..L"], ([(0,0), (0,1), (0,2)], [])),
    ([".L.", "***"], ([], [(1,0), (1,1), (1,2)])),
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
     ], ([(1,9), (5,2), (7,9)], [(3,5), (5,6), (7,2)]))
])
def test_finding_items(grid_list, expected):
    assert finding_items(grid_list) == expected

