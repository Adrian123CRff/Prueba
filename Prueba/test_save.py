# test_save.py
from api_client import ApiClient
from state_initializer import init_game_state
from save_manager import save_game, load_game, list_saves

def test_save_load():
    api = ApiClient()
    state = init_game_state(api)

    # Guardar partida
    save_game(state, "slot1.sav")

    # Listar saves
    print("Saves disponibles:", list_saves())

    # Cargar partida
    loaded_state = load_game("slot1.sav")
    if loaded_state:
        print("Partida cargada correctamente")
        print(f"Jugador: {loaded_state.player['name']} | Dinero: {loaded_state.player['money']}")
        print(f"Pedidos cargados: {len(loaded_state.orders)}")
        print(f"Clima cargado: {loaded_state.weather_state['summary']}")

if __name__ == "__main__":
    test_save_load()
