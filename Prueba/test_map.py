# test_map.py
import arcade
from api_client import ApiClient
from state_initializer import init_game_state
from map_manager import GameMap
from player_manager import Player

SCREEN = 800
TILE_SIZE = 20

class MapTestView(arcade.View):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.game_map = GameMap(state.city_map)
        # Crear jugador en posición central
        self.player = Player(start_x=0, start_y=0, tile_size=TILE_SIZE)

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text(f"Mapa: {self.game_map.name}", 10, SCREEN - 20,
                         arcade.color.WHITE, 16)
        self.game_map.draw_debug(tile_size=TILE_SIZE)
        self.player.draw()

    def on_key_press(self, key, modifiers):
        dx = dy = 0
        if key == arcade.key.UP:
            dy = 1
        elif key == arcade.key.DOWN:
            dy = -1
        elif key == arcade.key.LEFT:
            dx = -1
        elif key == arcade.key.RIGHT:
            dx = 1
        if dx or dy:
            self.player.move(dx, dy, self.game_map)

def main():
    api = ApiClient()
    state = init_game_state(api)

    window = arcade.Window(SCREEN, SCREEN, "Test Mapa y Jugador")
    view = MapTestView(state)
    window.show_view(view)
    arcade.run()

if __name__ == "__main__":
    main()
