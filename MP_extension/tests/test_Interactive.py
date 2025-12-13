from classes import Interactive

def test_Interactive_all(tmp_path):
    # Map layout
    content = (
        "TTTTTTTTT\n"
        "T...+...T\n"
        "T..R~...T\n"
        "T.TRR.T.T\n"
        "T.T.LTT.T\n"
        "T.x...*.T\n"
        "T.......T\n"
        "T..~....T\n"
        "TTTTTTTTT"
    )

    file_path = tmp_path / "testmap.txt"
    file_path.write_text(content)

    game = Interactive(str(file_path))


    # Initial state checks
    assert game.player_loc == (4, 4)
    assert game.mushroom_count == 1
    assert game.current_mushroom == 0
    assert game.state is None
    assert game.held_items is None
    assert game.previous_loc == "."




    # Pick up axe 'x' at (5,2)
    moves_to_axe = ["S", "A", "A"]  # Down, left, left
    for move in moves_to_axe:
        game.handle_movement(move, silent=True)
    assert game.previous_loc == "x"       # underlying tile
    game.handle_pickup()
    assert game.held_items == "x"
    assert game.previous_loc == "."
    assert game.player_loc == (5, 2)

    # Move up to cut tree at (4,2)
    game.handle_movement("W", silent=True)
    assert game.held_items is None
    assert game.playing_map[4][2] == "L"  
    assert game.player_loc == (4, 2)
    assert game.previous_loc == "."




    # Pick up flamethrower '*' at (5,6)
    moves_to_fire = ["S", "D", "D", "D", "D"]  
    for move in moves_to_fire:
        game.handle_movement(move, silent=True)
    game.handle_pickup()
    assert game.held_items == "*"
    assert game.player_loc == (5, 6)
    assert game.previous_loc == "."

    # Burn tree at (4,6)
    game.handle_movement("W", silent=True)
    assert game.held_items is None
    assert game.playing_map[4][6] == "L"  # tree burned
    assert game.player_loc == (4, 6)
    assert game.previous_loc == "."




    # Collect mushroom at (1,4)
    moves_to_mushroom = ["A", "A", "W", "W", "W"] 
    for move in moves_to_mushroom:
        game.handle_movement(move, silent=True)
    assert game.current_mushroom == 1
    assert game.state is True               # win condition
    assert game.player_loc == (1, 4)
    assert game.previous_loc == "."



    # New Game
    game1 = Interactive(str(file_path))

    # Rock pushing tests
    # Attempt to push rock right onto water tile
    game1.handle_movement("W", silent=True)
    assert game1.playing_map[3][4] == "L"  # player moved
    assert game1.playing_map[2][4] == "_"  # rock moved one
    assert game1.previous_loc == "."
    assert game1.player_loc == (3, 4)

    # Attempt to push rock right into tree (blocked)
    game1.handle_movement("A", silent=True)
    # Player shouldn't move because tree is blocking
    assert game1.player_loc == (3, 4)
    assert game1.previous_loc == "."
    assert game1.playing_map[3][3] == "R"
    assert game1.playing_map[3][2] == "T"

    # Pushing rock into another rock
    moves_to_rock = ["S", "A", "W"] 
    for move in moves_to_rock:
        game1.handle_movement(move, silent=True)
    # Player shouldn't move because there are two rocks in front
    assert game1.player_loc == (4, 3)
    assert game1.previous_loc == "."
    assert game1.playing_map[3][3] == "R"
    assert game1.playing_map[2][3] == "R"


    # Falling in water (losing test)
    # Move player above water
    moves_to_water = ["S"] * 3 
    for move in moves_to_water:
        game1.handle_movement(move, silent=True)
    assert game1.player_loc == (7, 3)
    assert game1.previous_loc == "."
    assert game1.playing_map[7][3] == "~"
    assert game1.state is False       # moves into water, losing condition
