# debug_state_map.py
from api_client import ApiClient
from state_initializer import init_game_state

api = ApiClient()
print(">>> api.get_city_map() keys/type:")
m = api.get_city_map()
print("type:", type(m))
if isinstance(m, dict):
    print("top keys:", list(m.keys()))
    print("has tiles?:", "tiles" in m)
else:
    print(m)

print("\n>>> init_game_state() result keys/type:")
state = init_game_state(api)   # le pasamos el api explícitamente
print("state has attr city_map?:", hasattr(state, "city_map"))
cm = getattr(state, "city_map", None)
print("state.city_map type:", type(cm))
if isinstance(cm, dict):
    print("state.city_map top keys:", list(cm.keys()))
else:
    print(cm)
