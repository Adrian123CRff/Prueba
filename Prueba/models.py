# models.py

class GameState:
    def __init__(self, player, city_map, orders, weather_state, reputation):
        self.player = player
        self.city_map = city_map      # ✅ nombre consistente
        self.orders = orders
        self.weather_state = weather_state
        self.reputation = reputation

    def to_dict(self):
        return {
            "player": self.player,
            "city_map": self.city_map,   # ✅ mantener el nombre al guardar
            "orders": self.orders,
            "weather_state": self.weather_state,
            "reputation": self.reputation,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            player=data.get("player", {}),
            city_map=data.get("city_map", {}),   # ✅ consistente
            orders=data.get("orders", []),
            weather_state=data.get("weather_state", {}),
            reputation=data.get("reputation", 0),
        )
