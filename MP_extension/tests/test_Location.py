from classes import Locations

def test_Locations(tmp_path):
    content = (
        "TTTTTTTTT\n"
        "T...+...T\n"
        "T...~...T\n"
        "T...R.T.T\n"
        "T.T.LTT.T\n"
        "T.x...*.T\n"
        "T.......T\n"
        "T.......T\n"
        "TTTTTTTTT"
    )

    file_path = tmp_path / "testmap.txt"
    file_path.write_text(content)

    loc = Locations(str(file_path))

    # test find_L
    loc.find_L()
    assert loc.player_loc == (4, 4)

    # test find_items
    loc.find_items()
    assert loc.items_loc[0] == [(5, 2)]   # axe
    assert loc.items_loc[1] == [(5, 6)]   # flamethrower

    # test count_mushroom
    loc.count_mushroom()
    assert loc.mushroom_count == 1
