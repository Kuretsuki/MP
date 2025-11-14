import pytest
from game_main_controls import handle_pickup

@pytest.mark.parametrize(
    "previous_loc,current_loc,axes_loc,fires_loc,held_items,expected",
    [
    # Tests for exhausted possibilities
        # User is on an axe and pressed [P]
        ("x", (1,2), {(1,2)}, set(), None, (".", "x", "You picked up an axe!")),

        # User is on a flamethrower and pressed [P]
        ("*", (1,2), set(), {(1,2)}, None, (".", "*", "You picked up a flamethrower!")),


        # User pressed [P] on a tile that has no item
        # Empty tile
        (".", (1,2), set({(1,3)}), set({(1,4)}), None, (".", None, "There is no item to be picked up!")),

        # User pressed [P] on a tile that has no item
        # Paved tile
        ("_", (1,2), set({(1.3)}), set({(1,4)}), None, ("_", None, "There is no item to be picked up!")),


        # User pressed [P] but no item in the map
        (".", (1,2), set(), set(), None, (".", None, "There is no item to be picked up!")),
        ("_", (1,2), set(), set(), None, ("_", None, "There is no item to be picked up!")),


        # User pressed [P] while holding an item
        # Holding an axe and trying to pick-up another axe
        ("x", (1,2), {(1,2)}, set(), "x", ("x", "x", "You are already holding an item!")),

        # User pressed [P] while holding an item
        # Holding an axe and trying to pick-up a flamethrower
        ("*", (1,2), {(1,2)}, set(), "x", ("*", "x", "You are already holding an item!")),

        # User pressed [P] while holding an item
        # Holding a flamethrower and trying to pick-up another flamethrower
        ("*", (1,2), {(1,2)}, set(), "*", ("*", "*", "You are already holding an item!")),
        # User pressed [P] while holding an item
        # Holding a flamethrower and trying to pick-up an axe
        ("x", (1,2), {(1,2)}, set(), "*", ("x", "*", "You are already holding an item!")),

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
