# test_map.py
import arcade
from api_client import ApiClient
from state_initializer import init_game_state
from map_manager import GameMap

SCREEN_SIZE = 800
TILE_SIZE = 20

class MapTestView(arcade.View):
    def __init__(self, state):
        super().__init__()
        self.state = state

        # Si por alguna razon state.city_map es vacío, intentar obtenerlo del API
        if not getattr(state, "city_map", None):
            print("[TEST_MAP] state.city_map vacío, intentar usar ApiClient directamente...")
            api = ApiClient()
            state.city_map = api.get_city_map() or {}

        # Mostrar información de debug sobre el objeto que vamos a usar
        print(">>> DEBUG antes de crear GameMap:")
        print("state.city_map type:", type(state.city_map))
        if isinstance(state.city_map, dict):
            print("state.city_map keys:", list(state.city_map.keys()))
            print("has tiles?:", "tiles" in state.city_map)

        self.game_map = GameMap(state.city_map if isinstance(state.city_map, dict) else {})

        print("=== DEBUG: GameMap summary ===")
        print("Name:", self.game_map.name)
        print("Size:", self.game_map.width, "x", self.game_map.height)
        print("Grid rows (len):", len(self.game_map.grid))
        if len(self.game_map.grid) > 0:
            print("Primera fila sample:", self.game_map.grid[0][:min(10, len(self.game_map.grid[0]))])
        print("=============================")

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text(f"Mapa: {self.game_map.name}", 10, SCREEN_SIZE - 20, arcade.color.WHITE, 16)
        self.game_map.draw_debug(tile_size=TILE_SIZE, draw_grid_lines=True)

def main():
    api = ApiClient()
    state = init_game_state(api)

    window = arcade.Window(SCREEN_SIZE, SCREEN_SIZE, "Test Mapa TigerCity")
    view = MapTestView(state)
    window.show_view(view)
    arcade.run()

if __name__ == "__main__":
    main()
