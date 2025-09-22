# ui_views.py
import arcade
from save_manager import list_saves, load_game, save_game
from state_initializer import init_game_state
from api_client import ApiClient

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Courier Quest"

# ----------- Main Menu View -----------
class MainMenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Courier Quest", SCREEN_WIDTH/2, SCREEN_HEIGHT-100,
                         arcade.color.WHITE, font_size=36, anchor_x="center")

        arcade.draw_text("Presiona ENTER para continuar", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Presiona ESC para salir", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 40,
                         arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game_menu = GameMenuView()
            self.window.show_view(game_menu)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

# ----------- Game Menu View -----------
class GameMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.saves = list_saves()

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Menú de Juego", SCREEN_WIDTH/2, SCREEN_HEIGHT-100,
                         arcade.color.WHITE, font_size=30, anchor_x="center")

        arcade.draw_text("1. Nueva Partida", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 40,
                         arcade.color.LIGHT_GREEN, 20, anchor_x="center")
        arcade.draw_text("2. Cargar Partida", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.LIGHT_GREEN, 20, anchor_x="center")
        arcade.draw_text("3. Retroceder", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 40,
                         arcade.color.LIGHT_GREEN, 20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.KEY_1:  # Nueva partida
            api = ApiClient()
            state = init_game_state(api)
            save_game(state, "slot1.sav")
            game_view = GameView(state)
            self.window.show_view(game_view)

        elif key == arcade.key.KEY_2:  # Cargar partida
            if self.saves:
                state = load_game(self.saves[0])  # cargar el más reciente
                if state:
                    game_view = GameView(state)
                    self.window.show_view(game_view)
            else:
                print("[INFO] No hay partidas guardadas")

        elif key == arcade.key.KEY_3:  # Retroceder
            self.window.show_view(MainMenuView())

# ----------- Game View -----------
class GameView(arcade.View):
    def __init__(self, state):
        super().__init__()
        self.state = state

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_GREEN)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Partida en curso", SCREEN_WIDTH/2, SCREEN_HEIGHT-100,
                         arcade.color.WHITE, 28, anchor_x="center")

        arcade.draw_text(f"Jugador: {self.state.player['name']}", 50, SCREEN_HEIGHT/2,
                         arcade.color.YELLOW, 20)
        arcade.draw_text(f"Pedidos: {len(self.state.orders)}", 50, SCREEN_HEIGHT/2 - 40,
                         arcade.color.YELLOW, 20)
        arcade.draw_text(f"Clima: {self.state.weather_state['summary']}", 50, SCREEN_HEIGHT/2 - 80,
                         arcade.color.YELLOW, 20)

# ----------- Main App -----------
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu = MainMenuView()
    window.show_view(menu)
    arcade.run()

if __name__ == "__main__":
    main()
