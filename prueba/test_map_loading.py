# tests/test_map_loading.py
from map_manager import GameMap
def test_tiles_loaded_from_cache():
    # usa un dict con tiles simple
    data = {"name":"T", "width":3, "height":3, "tiles":[["C","C","C"],["C","B","C"],["C","C","C"]]}
    gm = GameMap(data)
    assert gm.width == 3
    assert gm.grid[1][1] == "B"
