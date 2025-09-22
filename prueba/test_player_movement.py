# test_map_with_player.py
import arcade
from api_client import ApiClient
from state_initializer import init_game_state
from map_manager import GameMap, FLIP_Y
from player_manager import Player
from pathfinding import a_star  # opcional: usar sólo para preview; el jugador decide si seguir

SCREEN_SIZE = 800
TILE_SIZE = 24

class MapPlayerView(arcade.View):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.game_map = GameMap(state.city_map if getattr(state, "city_map", None) else {})
        rows = len(self.game_map.grid)
        cols = len(self.game_map.grid[0]) if rows>0 else 0

        # jugador en el centro
        start_cx = cols // 2
        start_cy = rows // 2
        self.player = Player((start_cx, start_cy), TILE_SIZE, rows, flip_y=FLIP_Y)

        # Flags y UX
        self.show_path_preview = True   # mostrar ruta calculada (si existe)
        self.path_preview = []          # ruta calculada (pero no seguida automáticamente)
        self.selected_job = None        # job seleccionado si lo hay

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        # dibujar mapa
        self.game_map.draw_debug(tile_size=TILE_SIZE, draw_grid_lines=True)

        # dibujar planned path preview (si hay)
        if self.show_path_preview and self.path_preview:
            for (i,(cx,cy)) in enumerate(self.path_preview):
                px = cx * TILE_SIZE + TILE_SIZE/2
                py = (len(self.game_map.grid)-1-cy) * TILE_SIZE + TILE_SIZE/2 if FLIP_Y else cy * TILE_SIZE + TILE_SIZE/2
                radius = TILE_SIZE * 0.18
                arcade.draw_circle_filled(px, py, radius, arcade.color.ALIZARIN_CRAYOLA if i == len(self.path_preview)-1 else arcade.color.SKY_BLUE)
                arcade.draw_circle_outline(px, py, radius, arcade.color.BLACK, 1)

        # dibujar planned_path (la plan del player)
        for (i,(cx,cy)) in enumerate(self.player.planned_path):
            px = cx * TILE_SIZE + TILE_SIZE/2
            py = (len(self.game_map.grid)-1-cy) * TILE_SIZE + TILE_SIZE/2 if FLIP_Y else cy * TILE_SIZE + TILE_SIZE/2
            arcade.draw_rectangle_outline(px, py, TILE_SIZE*0.6, TILE_SIZE*0.6, arcade.color.YELLOW, 2)

        # dibujar jugador
        self.player.draw()

        # HUD
        arcade.draw_text(f"Cell: ({self.player.cell_x},{self.player.cell_y})  Planned steps: {len(self.player.planned_path) - self.player.next_step_index}", 8, SCREEN_SIZE-20, arcade.color.WHITE, 14)

    def on_update(self, dt: float):
        self.player.update(dt)

    # MOVIMIENTO MANUAL CON FLECHAS (un paso adyacente)
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self._attempt_step(0, 1)
        elif key == arcade.key.DOWN:
            self._attempt_step(0, -1)
        elif key == arcade.key.LEFT:
            self._attempt_step(-1, 0)
        elif key == arcade.key.RIGHT:
            self._attempt_step(1, 0)
        elif key == arcade.key.SPACE:
            # ejecutar un step desde planned_path (si existe)
            moved = self.player.step_once()
            if not moved:
                print("No planned steps to execute.")
        elif key == arcade.key.P:
            # toggle preview visibility
            self.show_path_preview = not self.show_path_preview

    def _attempt_step(self, dx:int, dy:int):
        tx = self.player.cell_x + dx
        ty = self.player.cell_y + dy
        # límites
        if not (0 <= tx < self.game_map.width and 0 <= ty < self.game_map.height):
            print("Fuera de límites")
            return
        if not self.game_map.is_walkable(tx, ty):
            print("No transitable:", tx,ty, "tile:", self.game_map.grid[ty][tx])
            return
        # todo ok: solicitar paso
        self.player.request_step_to_cell(tx, ty)

    # CLICK: planificar ruta (calcula A* preview) — NO mover automáticamente
    def on_mouse_press(self, x, y, button, modifiers):
        # convertir a celda
        cx = int(x // TILE_SIZE)
        row_index = int(y // TILE_SIZE)
        cy = (len(self.game_map.grid)-1) - row_index if FLIP_Y else row_index

        # si clic fuera de mapa, ignorar
        if not (0 <= cx < self.game_map.width and 0 <= cy < self.game_map.height):
            return

        # si clic en celda adyacente: moverse 1 paso
        if abs(cx - self.player.cell_x) + abs(cy - self.player.cell_y) == 1:
            if self.game_map.is_walkable(cx, cy):
                self.player.request_step_to_cell(cx, cy)
            return

        # ellers: planificar ruta (preview) pero NO ejecutar
        path = a_star(self.game_map, (self.player.cell_x, self.player.cell_y), (cx, cy))
        if path:
            self.path_preview = path
            # plan para el player (pero no se ejecuta hasta que el jugador presione SPACE)
            self.player.plan_path(path)
            print("Ruta planificada; presiona SPACE para ejecutar paso a paso.")
        else:
            print("No hay camino hacia la celda seleccionada.")

def main():
    api = ApiClient()
    state = init_game_state(api)
    window = arcade.Window(SCREEN_SIZE, SCREEN_SIZE, "Mapa con Player (control manual)")
    view = MapPlayerView(state)
    window.show_view(view)
    arcade.run()

if __name__ == "__main__":
    main()
