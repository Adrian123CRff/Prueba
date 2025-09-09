# state_initializer.py
"""from models import GameState
from api_client import ApiClient

def init_game_state(api: ApiClient) -> GameState:

    Inicializa un estado de juego a partir de la API.
    Si algún endpoint falla, usará caché o datos locales.

    city_map = api.get_city_map()
    jobs = api.get_jobs()
    weather = api.get_weather()

    # Construir estado del jugador
    player = {
        "name": "Courier",
        "hp": 100,
        "stamina": 100,
        "position": [0, 0],
        "level": 1,
        "money": 0,
    }

    # Construir mundo
    world = {
        "map": city_map,
        "current_map": city_map.get("name", "TigerCity"),
        "time_played": 0,
        "goal_income": 500,   # por ejemplo, dinero para ganar
    }

    # Normalizar pedidos
    orders = []
    for job in jobs:
        orders.append({
            "id": job.get("id"),
            "pickup": job.get("pickup"),
            "dropoff": job.get("dropoff"),
            "reward": job.get("reward", 0),
            "deadline": job.get("deadline", None),
            "status": "available"
        })

    # Estado inicial del clima
    weather_state = {
        "condition": weather.get("condition", "unknown"),
        "summary": weather.get("summary", "Desconocido"),
        "temperature": weather.get("temperature", 20),
        "intensity": weather.get("intensity", 0.0)
    }

    # Retornar GameState completo
    return GameState(
        player=player,
        world=world,
        inventory=[],
        orders=orders,
        reputation=70,
        weather_state=weather_state
    )"""
# state_initializer.py
from models import GameState

def init_game_state(api_client):
    city_map = api_client.get_city_map()
    orders = api_client.get_jobs()
    weather = api_client.get_weather()

    player = {
        "name": "Courier",
        "hp": 100,
        "stamina": 100,
        "money": 0,
    }

    state = GameState(
        player=player,
        city_map=city_map,       # ✅ usar city_map
        orders=orders,
        weather_state=weather,
        reputation=70
    )
    return state
