import arcade
import arcade.gui

from api_client import ApiClient
from state_initializer import init_game_state
from save_manager import save_game, load_game, list_saves
from game_view import GameView

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Courier Quest"

# ========================
# Vista: Menú Principal
# ========================
class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Layout vertical
        v_box = arcade.gui.UIBoxLayout(vertical=True, space_between=20)

        # Botón: Continuar
        continue_btn = arcade.gui.UIFlatButton(text="Continuar", width=200)
        v_box.add(continue_btn)

        @continue_btn.event("on_click")
        def on_click_continue(event):
            self.window.show_view(GameMenuView())

        # Botón: Salir
        quit_btn = arcade.gui.UIFlatButton(text="Salir", width=200)
        v_box.add(quit_btn)

        @quit_btn.event("on_click")
        def on_click_quit(event):
            arcade.close_window()

        # Centrar todo
        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(child=v_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(anchor)

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_text("Courier Quest", SCREEN_WIDTH/2, SCREEN_HEIGHT-100,
                         arcade.color.WHITE, font_size=36, anchor_x="center")


# ========================
# Vista: Menú de Juego
# ========================
    class GameMenuView(arcade.View):
        def __init__(self):
            super().__init__()
            self.manager = arcade.gui.UIManager()
            self.manager.enable()

            v_box = arcade.gui.UIBoxLayout(vertical=True, space_between=20)

            # Botón Nueva Partida
            new_game_button = arcade.gui.UIFlatButton(text="Nueva Partida", width=200)
            v_box.add(new_game_button)

            @new_game_button.event("on_click")
            def on_click_new(event):
                api = ApiClient()
                state = init_game_state(api)
                save_game(state, "slot1.sav")  # guardar inmediatamente
                self.window.show_view(GameView(state))  # <--- AHORA CON STATE

            # Botón Cargar Partida
            load_button = arcade.gui.UIFlatButton(text="Cargar Partida", width=200)
            v_box.add(load_button)

            @load_button.event("on_click")
            def on_click_load(event):
                saves = list_saves()
                if saves:
                    state = load_game(saves[0])  # carga el primer slot
                    if state:
                        self.window.show_view(GameView(state))
                else:
                    print("[INFO] No hay partidas guardadas")

            # Botón Retroceder
            back_button = arcade.gui.UIFlatButton(text="Retroceder", width=200)
            v_box.add(back_button)

            @back_button.event("on_click")
            def on_click_back(event):
                from ui_views_gui import MainMenuView
                self.window.show_view(MainMenuView())

            # Centrar layout
            anchor = arcade.gui.UIAnchorLayout()
            anchor.add(child=v_box, anchor_x="center_x", anchor_y="center_y")
            self.manager.add(anchor)

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_text("Menú de Juego", SCREEN_WIDTH/2, SCREEN_HEIGHT-100,
                         arcade.color.WHITE, font_size=30, anchor_x="center")


# ========================
# Vista: Juego en curso
# ========================
class GameView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_GREEN)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Partida en curso", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.WHITE, 28, anchor_x="center")


# ========================
# Programa Principal
# ========================
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(MainMenuView())
    arcade.run()


if __name__ == "__main__":
    main()
