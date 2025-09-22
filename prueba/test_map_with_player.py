# test_map_with_player.py (corregido)
import arcade
from api_client import ApiClient
from state_initializer import init_game_state
from map_manager import GameMap, FLIP_Y  # si no exportas FLIP_Y, pon True/False aquí
from player_manager import Player
from pathfinding import a_star

SCREEN_SIZE = 800
TILE_SIZE = 24  # debe coincidir con el tile_size del Player

# helper: safe draw rectangle outline (fallback si arcade no lo tiene)
def safe_draw_rectangle_outline(cx, cy, width, height, color, border=1):
    try:
        # normalmente arcade tiene draw_rectangle_outline
        arcade.draw_rectangle_outline(cx, cy, width, height, color, border)
    except Exception:
        # fallback: dibujar dos líneas (no perfecto, pero funciona)
        x1 = cx - width/2
        y1 = cy - height/2
        x2 = cx + width/2
        y2 = cy + height/2
        arcade.draw_line(x1, y1, x2, y1, color, border)
        arcade.draw_line(x1, y2, x2, y2, color, border)
        arcade.draw_line(x1, y1, x1, y2, color, border)
        arcade.draw_line(x2, y1, x2, y2, color, border)


class MapPlayerView(arcade.View):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.game_map = GameMap(state.city_map if getattr(state, "city_map", None) else {})
        rows = len(self.game_map.grid)
        cols = len(self.game_map.grid[0]) if rows > 0 else 0

        # colocar jugador en centro
        start_cx = cols // 2
        start_cy = rows // 2

        # pasar game_map y callbacks al Player
        self.player = Player(
            (start_cx, start_cy),
            TILE_SIZE,
            rows,
            flip_y=FLIP_Y,
            game_map=self.game_map,
            on_blocked=self.on_player_blocked,
            on_step_complete=self.on_player_step_complete
        )

        self.path_preview = []  # ruta calculada (preview)
        self.show_preview = True

        # HUD pequeño (mensaje temporal)
        self._msg = None
        self._msg_ttl = 0.0

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        # dibujar mapa
        self.game_map.draw_debug(tile_size=TILE_SIZE, draw_grid_lines=True)

        # preview path (si existe)
        if self.show_preview and self.path_preview:
            for i, (cx, cy) in enumerate(self.path_preview):
                px = cx * TILE_SIZE + TILE_SIZE / 2
                py = (len(self.game_map.grid) - 1 - cy) * TILE_SIZE + TILE_SIZE / 2 if FLIP_Y else cy * TILE_SIZE + TILE_SIZE / 2
                r = TILE_SIZE * 0.18
                # usar la referencia completa arcade.color
                color = arcade.color.SKY_BLUE if i < len(self.path_preview) - 1 else arcade.color.RED
                arcade.draw_circle_filled(px, py, r, color)

        # draw planned_path boxes (player.planned_path)
        for (cx, cy) in getattr(self.player, "planned_path", []):
            px = cx * TILE_SIZE + TILE_SIZE / 2
            py = (len(self.game_map.grid) - 1 - cy) * TILE_SIZE + TILE_SIZE / 2 if FLIP_Y else cy * TILE_SIZE + TILE_SIZE / 2
            # usar helper seguro para outline
            safe_draw_rectangle_outline(px, py, TILE_SIZE * 0.6, TILE_SIZE * 0.6, arcade.color.YELLOW, 2)

        # dibujar player
        self.player.draw()

        # HUD
        arcade.draw_text(
            f"Cell: ({self.player.cell_x},{self.player.cell_y})  Planned left: {max(0, len(self.player.planned_path) - self.player.next_step_index)}",
            8, SCREEN_SIZE - 20, arcade.color.WHITE, 14
        )

        # mensaje temporal de HUD si existe
        if self._msg and self._msg_ttl > 0:
            arcade.draw_text(self._msg, 10, SCREEN_SIZE - 40, arcade.color.LIGHT_GRAY, 12)

    def on_update(self, dt):
        # decrementar TTL de mensajes
        if self._msg_ttl > 0:
            self._msg_ttl -= dt
            if self._msg_ttl <= 0:
                self._msg = None
        self.player.update(dt)

    def on_key_press(self, key, modifiers):
        if self.player.moving:
            # bloquear nuevos pasos mientras está en interpolación
            return
        if key == arcade.key.UP:
            self._try_adjacent(0, 1)
        elif key == arcade.key.DOWN:
            self._try_adjacent(0, -1)
        elif key == arcade.key.LEFT:
            self._try_adjacent(-1, 0)
        elif key == arcade.key.RIGHT:
            self._try_adjacent(1, 0)
        elif key == arcade.key.SPACE:
            moved = self.player.step_once()
            if not moved:
                self._set_msg("No hay pasos planificados o paso bloqueado.", 1.8)
        elif key == arcade.key.P:
            self.show_preview = not self.show_preview

    def _try_adjacent(self, dx, dy):
        tx = self.player.cell_x + dx
        ty = self.player.cell_y + dy
        ok, reason = self.player.request_step_to_adjacent(tx, ty)
        if not ok:
            self._set_msg(f"No puedes moverte: {reason}", 1.6)

    def on_mouse_press(self, x, y, button, modifiers):
        # convertir pixel a celda (si usas camera, convertir coordenadas primero)
        # si tienes cámara: world_x, world_y = self.camera.screen_to_world(x, y)
        cx = int(x // TILE_SIZE)
        row_idx = int(y // TILE_SIZE)
        cy = (len(self.game_map.grid) - 1) - row_idx if FLIP_Y else row_idx

        if not (0 <= cx < self.game_map.width and 0 <= cy < self.game_map.height):
            return

        # si clic adyacente: moverse 1 paso
        if abs(cx - self.player.cell_x) + abs(cy - self.player.cell_y) == 1:
            ok, reason = self.player.request_step_to_adjacent(cx, cy)
            if not ok:
                self._set_msg(f"No puedes moverte: {reason}", 1.2)
            return

        # calcular ruta (preview) y planificar (no ejecutar)
        path = a_star(self.game_map, (self.player.cell_x, self.player.cell_y), (cx, cy))
        if path:
            self.path_preview = path
            self.player.plan_path(path)
            self._set_msg("Ruta planificada. Presiona SPACE para ejecutar un paso.", 2.5)
        else:
            self.path_preview = []
            self._set_msg("No hay camino a la celda seleccionada.", 2.0)

    # ----- callbacks requeridos por Player (antes daban AttributeError) -----
    def on_player_blocked(self, x: int, y: int, reason: str):
        """Callback cuando Player intenta un paso y está bloqueado."""
        # muestra un mensaje en HUD y log en consola
        self._set_msg(f"Bloqueado en ({x},{y}): {reason}", 2.0)
        print("[Player blocked]", x, y, reason)

    def on_player_step_complete(self, x: int, y: int):
        """Callback cuando Player completa un paso."""
        self._set_msg(f"Llegaste a ({x},{y})", 1.0)
        # aquí podrías triggerar eventos (pickups, checks de job)...
        print("[Player step complete]", x, y)

    def _set_msg(self, text: str, ttl: float = 1.5):
        self._msg = text
        self._msg_ttl = ttl


def main():
    api = ApiClient()
    state = init_game_state(api)
    window = arcade.Window(SCREEN_SIZE, SCREEN_SIZE, "Mapa con Player (control manual)")
    view = MapPlayerView(state)
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()

