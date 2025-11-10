import pytest
from map_tracking import mapp

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
    ("m3.txt", ".L.\n.R.", [".L.", ".R."]  )
])

def test_mapp(filename, tmp_path, content, expected):
    file_path = tmp_path / filename
    file_path.write_text(content)
    assert mapp(file_path) == expected
