import pytest
from game_display import load_mapp

@pytest.mark.parametrize("grid_list, expected",[
    (["TTTTTT"], "🌲🌲🌲🌲🌲🌲"),
    (["LR...."], "🧑🪨        "),
    (["T.++T*"], "🌲  🍄🍄🌲🔥"),
    (["Lx...~"], "🧑🪓      🟦"),
    (["..R_.."], "    🪨🟥    "),
])


def test_load_mapp(grid_list, expected):
    assert load_mapp(grid_list) == expected