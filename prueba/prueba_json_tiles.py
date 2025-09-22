from api_client import ApiClient
import json
from pathlib import Path

api = ApiClient()
m = api.get_city_map()
print("Top keys:", list(m.keys()))
print("len(buildings):", len(m.get("buildings", [])))
print("len(roads):", len(m.get("roads", [])))
print("buildings sample (first 5):")
import pprint; pp = pprint.PrettyPrinter(depth=2, width=120)
pp.pprint(m.get("buildings", [])[:5])
print("roads sample (first 5):")
pp.pprint(m.get("roads", [])[:5])
print("legend:", m.get("legend"))




p = Path("api_cache") / "city_map.json"
print("cache exists:", p.exists())
if p.exists():
    data = json.load(p.open(encoding="utf-8"))
    import pprint
    pprint.pprint({k: (type(v).__name__, (len(v) if isinstance(v,(list,dict)) else None)) for k,v in data.items()})
    # si hay "tiles", imprime fila 0
    if "tiles" in data:
        print("tiles first row sample:", data["tiles"][0][:10])




