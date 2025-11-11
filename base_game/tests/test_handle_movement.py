import pytest
from game_main_controls import handle_movement

@pytest.mark.parametrize(
    "grid, x, y, dx, dy, prev_loc, current_mush, mushrooms, expected_current_loc, expected_prev, expected__current_mush",
    [
        ([['.', '.'], ['.', '.']], 0, 0, 1, 0, '.', 0, 0, (1,0), '.', 0),
        ([['.', '.'], ['.', '.']], 1, 0, 0, 1, '.', 0, 0, (1,1), '.', 0),
        ([['.', '+'], ['.', '.']], 0, 0, 0, 1, '.', 0, 1, (0,1), '.', 1),
        ([['.', 'L'], ['.', '.']], 0, 1, 0, -1, '.', 1, 1, (0,0), '.', 1),
    ]
)
def test_movement_only(mocker, grid, x, y, dx, dy, prev_loc, current_mush, mushrooms,
                       expected_current_loc, expected_prev, expected__current_mush):
    mocker.patch("game_main_controls.clear")
    mocker.patch("game_main_controls.load_mapp")
    mocker.patch("time.sleep", return_value=None)

    current_loc, previous_loc, held_items_out, current_mush, _, _ = handle_movement(
        grid, x, y, dx, dy, None, prev_loc, current_mush, mushrooms
    )

    assert current_loc == expected_current_loc
    assert previous_loc == expected_prev
    assert current_mush == expected__current_mush
