# map_manager.py
import arcade

# Diccionario de traducción de símbolos -> propiedades
TILE_DEFS = {
    "C": {"name": "Calle", "walkable": True, "speed": 1.0, "color": arcade.color.LIGHT_GRAY},
    "R": {"name": "Carretera", "walkable": True, "speed": 1.5, "color": arcade.color.DARK_GRAY},
    "B": {"name": "Edificio", "walkable": False, "speed": 0, "color": arcade.color.DARK_BROWN},
    "P": {"name": "Parque", "walkable": True, "speed": 0.8, "color": arcade.color.DARK_GREEN},
    "W": {"name": "Agua", "walkable": False, "speed": 0, "color": arcade.color.BLUE},
    # fallback para caracteres desconocidos
    "?": {"name": "Desconocido", "walkable": False, "speed": 0, "color": arcade.color.RED},
}

class GameMap:
    def __init__(self, map_data: dict):
        """
        Carga un mapa desde el JSON devuelto por la API.
        map_data debe contener: name, width, height, map (matriz de símbolos).
        """
        self.name = map_data.get("name", "Unknown")
        self.width = map_data.get("width", 0)
        self.height = map_data.get("height", 0)
        self.grid = map_data.get("map", [])

    def is_walkable(self, x: int, y: int) -> bool:
        """Devuelve True si la celda se puede transitar."""
        if 0 <= x < self.width and 0 <= y < self.height:
            symbol = self.grid[y][x]
            return TILE_DEFS.get(symbol, TILE_DEFS["?"])["walkable"]
        return False

    def get_speed(self, x: int, y: int) -> float:
        """Devuelve la velocidad relativa en esta celda."""
        if 0 <= x < self.width and 0 <= y < self.height:
            symbol = self.grid[y][x]
            return TILE_DEFS.get(symbol, TILE_DEFS["?"])["speed"]
        return 0

    def draw_debug(self, tile_size: int = 20):
        """
        Dibuja el mapa como una cuadrícula coloreada.
        Cada símbolo se traduce a un color en TILE_DEFS.
        """
        for y in range(self.height):
            for x in range(self.width):
                symbol = self.grid[y][x]
                props = TILE_DEFS.get(symbol, TILE_DEFS["?"])
                color = props["color"]

                arcade.draw_rectangle_filled(
                    x * tile_size + tile_size / 2,
                    y * tile_size + tile_size / 2,
                    tile_size,
                    tile_size,
                    color
                )
