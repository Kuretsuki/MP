import pytest
from map_tracking import finding_L

@pytest.mark.parametrize("grid_list, expected", [
    ([], None),
    ([".L.", ".R."], (0, 1)),
    (["L..", "..."], (0, 0)),
    (["...", "..L"], (1, 2))
])
def test_finding_L(grid_list, expected):
    assert finding_L(grid_list) == expected

