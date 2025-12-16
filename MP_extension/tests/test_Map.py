import pytest
from classes import Map

@pytest.mark.parametrize("filename, content, expected", [
    ("m0.txt", "", []),

    ("m1.txt", "...\n.L.\n...", ["...", ".L.", "..."]),

    ("m2.txt",
     "TTTTTTTTT\n"
     "T...+..+T\n"
     "T+..~...T\n"
     "T...R.T.T\n"
     "T.T.LTT.T\n"
     "T.x...*.T\n"
     "T.......T\n"
     "T.......T\n"
     "TTTTTTTTT",
     [
         "TTTTTTTTT",
         "T...+..+T",
         "T+..~...T",
         "T...R.T.T",
         "T.T.LTT.T",
         "T.x...*.T",
         "T.......T",
         "T.......T",
         "TTTTTTTTT"
     ]),
])
def test_map_get_map(filename, tmp_path, content, expected):
    file_path = tmp_path / filename
    file_path.write_text(content)

    m = Map(str(file_path))        
    grid = m.get_map()           

    result = ["".join(row) for row in grid] 

    assert result == expected
