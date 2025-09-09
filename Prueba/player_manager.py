# player_manager.py
import arcade

PLAYER_SPEED = 5

class Player:
    def __init__(self, start_x, start_y, tile_size=20, color=arcade.color.YELLOW):
        self.x = start_x
        self.y = start_y
        self.tile_size = tile_size
        self.color = color

    def draw(self):
        arcade.draw_rectangle_filled(
            self.x * self.tile_size + self.tile_size / 2,
            self.y * self.tile_size + self.tile_size / 2,
            self.tile_size * 0.8,
            self.tile_size * 0.8,
            self.color
        )

    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy
        if game_map.is_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y
