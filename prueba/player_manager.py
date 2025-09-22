# player_manager.py
"""
Player manager enfocado en control manual.
- Soporta: step-by-step (player.step_once()), plan_path() (preview), step to adjacent cell, teleport.
- Opcional: pasar game_map (instancia GameMap) para validar transitable usando game_map.is_walkable.
- No mueve automáticamente a lo largo de toda la ruta: el jugador debe confirmar cada paso (space / UI).
"""

from typing import List, Tuple, Callable, Optional

# Ajusta velocidad de interpolación (pixeles / segundo)
PLAYER_SPEED_PIXELS_PER_SEC = 140.0

Cell = Tuple[int, int]


class Player:
    def __init__(
        self,
        start_cell: Cell,
        tile_size: int,
        map_rows: int,
        flip_y: bool = True,
        game_map=None,
        on_blocked: Optional[Callable[[int,int,str], None]] = None,
        on_step_complete: Optional[Callable[[int,int], None]] = None
    ):
        """
        start_cell: (cx, cy)
        tile_size: tamaño en píxeles de una celda
        map_rows: número de filas (height) del grid, necesario si flip_y==True
        flip_y: True si la fila 0 debe dibujarse en la parte superior
        game_map: instancia de GameMap (opcional). Si se pasa, se valida is_walkable antes de planificar/solicitar pasos.
        on_blocked(x,y,reason): callback cuando se intenta un paso y no es posible.
        on_step_complete(x,y): callback cuando el player completa un paso y queda en la nueva celda.
        """
        self.cell_x, self.cell_y = int(start_cell[0]), int(start_cell[1])
        self.tile_size = tile_size
        self.map_rows = map_rows
        self.flip_y = flip_y
        self.game_map = game_map

        # posición en píxeles (centro)
        self.pixel_x, self.pixel_y = self.cell_to_pixel(self.cell_x, self.cell_y)
        self.target_pixel_x, self.target_pixel_y = self.pixel_x, self.pixel_y
        self.moving: bool = False

        # planned path (lista de celdas). NO se sigue automáticamente.
        self.planned_path: List[Cell] = []
        self.next_step_index: int = 0  # índice del siguiente paso pendiente (en planned_path)

        # callbacks
        self.on_blocked = on_blocked
        self.on_step_complete = on_step_complete

        # apariencia (puedes cambiarlo desde la vista)
        self.radius = tile_size * 0.35
        self.color = (160, 82, 45)  # auburn-ish, o arcade.color.AUBURN

    # ---------------- coordinate helpers ----------------
    def cell_to_pixel(self, cx: int, cy: int) -> Tuple[float, float]:
        """Convierte (cx,cy) a coordenadas de píxel (centro de celda)."""
        px = cx * self.tile_size + self.tile_size / 2
        if self.flip_y:
            py = (self.map_rows - 1 - cy) * self.tile_size + self.tile_size / 2
        else:
            py = cy * self.tile_size + self.tile_size / 2
        return px, py

    def pixel_to_cell(self, px: float, py: float) -> Cell:
        """Convierte coordenadas de píxel a celda (ints)."""
        cx = int(px // self.tile_size)
        if self.flip_y:
            row_index = int(py // self.tile_size)
            cy = (self.map_rows - 1) - row_index
        else:
            cy = int(py // self.tile_size)
        return cx, cy

    # ---------------- planning API (manual control) ----------------
    def plan_path(self, path: List[Cell]):
        """
        Recibe una ruta (lista de celdas). NO la ejecuta automáticamente.
        Normaliza la ruta: si el primer nodo es la celda actual, lo quita.
        """
        if not path:
            self.planned_path = []
            self.next_step_index = 0
            return

        # quitar primer si es la celda actual
        if path[0] == (self.cell_x, self.cell_y):
            path = path[1:]
        self.planned_path = list(path)
        self.next_step_index = 0

    def clear_plan(self):
        self.planned_path = []
        self.next_step_index = 0

    # ---------------- single-step execution (player confirms) ----------------
    def step_once(self) -> bool:
        """
        Ejecuta un paso de la ruta planificada (si existe).
        Devuelve True si se inició un movimiento, False si no había pasos o estaba bloqueado.
        """
        if not self.planned_path:
            return False
        if self.next_step_index >= len(self.planned_path):
            return False

        nx, ny = self.planned_path[self.next_step_index]
        # validación: adyacencia (safety)
        if abs(nx - self.cell_x) + abs(ny - self.cell_y) != 1:
            # Si la ruta contiene un salto no adyacente, rechazar: el paso debe ser adyacente
            reason = "step_not_adjacent"
            if self.on_blocked:
                self.on_blocked(nx, ny, reason)
            return False

        # validar límites y walkable si tenemos game_map
        if self.game_map:
            if not (0 <= nx < self.game_map.width and 0 <= ny < self.game_map.height):
                reason = "out_of_bounds"
                if self.on_blocked:
                    self.on_blocked(nx, ny, reason)
                return False
            if not self.game_map.is_walkable(nx, ny):
                reason = "blocked_by_tile"
                if self.on_blocked:
                    self.on_blocked(nx, ny, reason)
                return False

        # Si todo ok, iniciar movimiento a la celda siguiente
        self.target_pixel_x, self.target_pixel_y = self.cell_to_pixel(nx, ny)
        self.moving = True
        # incrementamos índice: cuando llegue, será el siguiente a ejecutar
        self.next_step_index += 1
        return True

    # ---------------- immediate adjacent step (p.ej. flechas) ----------------
    def request_step_to_adjacent(self, nx: int, ny: int) -> Tuple[bool, Optional[str]]:
        """
        Solicita moverse a una celda adyacente inmediatamente (one-step).
        Valida límites y si el tile es transitable (si game_map se pasa).
        Retorna (True, None) si el movimiento fue aceptado (comienza), (False, razón_str) si no.
        """
        if abs(nx - self.cell_x) + abs(ny - self.cell_y) != 1:
            return False, "not_adjacent"

        if self.game_map:
            if not (0 <= nx < self.game_map.width and 0 <= ny < self.game_map.height):
                return False, "out_of_bounds"
            if not self.game_map.is_walkable(nx, ny):
                return False, "blocked_by_tile"

        # start move
        self.target_pixel_x, self.target_pixel_y = self.cell_to_pixel(nx, ny)
        self.moving = True
        return True, None

    # ---------------- teleport (load/save) ----------------
    def teleport_to(self, cx: int, cy: int):
        """Colocar al player inmediatamente en una celda (sin interpolación)."""
        self.cell_x, self.cell_y = int(cx), int(cy)
        self.pixel_x, self.pixel_y = self.cell_to_pixel(self.cell_x, self.cell_y)
        self.target_pixel_x, self.target_pixel_y = self.pixel_x, self.pixel_y
        self.moving = False
        self.planned_path = []
        self.next_step_index = 0

    # ---------------- update / draw ----------------
    def update(self, dt: float):
        """Interpolación hacia target. Si llega, actualiza (cell_x,cell_y) y llama callback on_step_complete."""
        if not self.moving:
            return

        dx = self.target_pixel_x - self.pixel_x
        dy = self.target_pixel_y - self.pixel_y
        dist = (dx * dx + dy * dy) ** 0.5
        if dist < 0.5:
            # llegó a destino
            self.pixel_x, self.pixel_y = self.target_pixel_x, self.target_pixel_y
            # actualizar cell indices basados en pixel (más seguro)
            cx, cy = self.pixel_to_cell(self.pixel_x, self.pixel_y)
            self.cell_x, self.cell_y = int(cx), int(cy)
            self.moving = False
            if self.on_step_complete:
                self.on_step_complete(self.cell_x, self.cell_y)
            return

        # avanzar
        step = PLAYER_SPEED_PIXELS_PER_SEC * dt
        t = min(1.0, step / dist)
        self.pixel_x += dx * t
        self.pixel_y += dy * t

    def draw(self, draw_fn: Optional[Callable] = None):
        """
        Dibuja al player. Por defecto usa arcade.draw_circle_filled; si tu entorno no tiene arcade en este módulo,
        puedes pasar un draw_fn(pixel_x, pixel_y, radius, color).
        """
        try:
            import arcade
            arcade.draw_circle_filled(self.pixel_x, self.pixel_y, self.radius, self.color)
            arcade.draw_circle_outline(self.pixel_x, self.pixel_y, self.radius, arcade.color.BLACK, 2)
        except Exception:
            # fallback usando draw_fn si se proporcionó
            if draw_fn:
                draw_fn(self.pixel_x, self.pixel_y, self.radius, self.color)
            else:
                # nada que hacer si no hay modo de dibujar
                pass
