# pathfinding.py
import heapq
from typing import List, Tuple, Optional, Dict

Cell = Tuple[int, int]

def manhattan(a: Cell, b: Cell) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbors(cell: Cell):
    x,y = cell
    return [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]

def reconstruct(came_from: Dict[Cell, Cell], current: Cell):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def a_star(game_map, start: Cell, goal: Cell) -> Optional[List[Cell]]:
    if start == goal:
        return [start]
    sx, sy = start; gx, gy = goal
    if not (0 <= sx < game_map.width and 0 <= sy < game_map.height):
        return None
    if not (0 <= gx < game_map.width and 0 <= gy < game_map.height):
        return None
    if not game_map.is_walkable(gx, gy):
        return None

    open_heap = []
    gscore = {start: 0}
    heapq.heappush(open_heap, (manhattan(start, goal), 0, start))
    came_from = {}
    closed = set()

    while open_heap:
        f, g, current = heapq.heappop(open_heap)
        if current in closed:
            continue
        if current == goal:
            return reconstruct(came_from, current)
        closed.add(current)

        for n in neighbors(current):
            nx, ny = n
            if not (0 <= nx < game_map.width and 0 <= ny < game_map.height):
                continue
            if not game_map.is_walkable(nx, ny):
                continue
            tentative_g = g + 1
            if tentative_g < gscore.get(n, 10**9):
                came_from[n] = current
                gscore[n] = tentative_g
                heapq.heappush(open_heap, (tentative_g + manhattan(n, goal), tentative_g, n))
    return None
