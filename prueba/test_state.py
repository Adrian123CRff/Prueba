# test_state.py
from api_client import ApiClient
from state_initializer import init_game_state

def test_state():
    api = ApiClient()
    state = init_game_state(api)

    print("=== Estado inicial del juego ===")
    print(f"Jugador: {state.player['name']} | HP={state.player['hp']} | Stamina={state.player['stamina']}")
    print(f"Mapa: {state.world['current_map']} ({state.world['map'].get('width')}x{state.world['map'].get('height')})")
    print(f"Pedidos disponibles: {len(state.orders)}")
    if state.orders:
        for i, order in enumerate(state.orders[:3]):  # mostrar solo 3 pedidos
            print(f"  - Pedido {order['id']} | Pickup={order['pickup']} → Dropoff={order['dropoff']} | Reward={order['reward']}")
    print(f"Clima: {state.weather_state['summary']} ({state.weather_state['condition']}), "
          f"{state.weather_state['temperature']}°C")
    print(f"Reputación inicial: {state.reputation}")

if __name__ == "__main__":
    test_state()
