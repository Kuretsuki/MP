import pytest
from game_main_controls import handle_pickup

@pytest.mark.parametrize(
    "previous_loc,current_loc,axes_loc,fires_loc,held_items,expected",
    [
        ("x", (1,2), {(1,2)}, set(), None, (".", "x", "You picked up an axe!")),
        ("*", (1,2), set(), {(1,2)}, None, (".", "*", "You picked up a flamethrower!")),
        (".", (1,2), set(), set(), None, (".", None, "There is no item to be picked up!")),
        ("x", (1,2), {(1,2)}, set(), "x", ("x", "x", "You are already holding an item!")),
    ]
)

def test_handle_pickup(previous_loc, current_loc, axes_loc, fires_loc, held_items, expected):
    grid = [list("....."), list("..L.."), list(".....")]

    axes_list = list(axes_loc)
    fires_list = list(fires_loc)

    result = handle_pickup(previous_loc, current_loc, axes_list, fires_list, held_items, grid)
    assert result == expected

    x, y = current_loc
    assert grid[x][y] == "L"
