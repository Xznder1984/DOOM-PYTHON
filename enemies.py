"""
ENEMIES - Pac-Man style ghosts
==============================
Keep all enemy settings here so they're easy to tweak.
"""
import random

# Colors per ghost (classic Pac-Man ghost colors)
ENEMY_TYPES = {
    "blinky": {"color": (255, 0, 0), "name": "Blinky", "speed": 1.2, "chase_chance": 0.25},
    "pinky":  {"color": (255, 184, 255), "name": "Pinky",  "speed": 1.15, "chase_chance": 0.25},
    "inky":   {"color": (0, 255, 255), "name": "Inky",   "speed": 1.18, "chase_chance": 0.25},
    "clyde":  {"color": (255, 184, 82), "name": "Clyde",  "speed": 1.1, "chase_chance": 0.25},
}

# Where ghosts start (in world pixels). We'll auto-place them if not set.
ENEMY_STARTS = [
    (420.0, 180.0, "blinky"),
    (480.0, 180.0, "pinky"),
    (420.0, 240.0, "inky"),
    (480.0, 240.0, "clyde"),
]

# How big ghosts appear in the world
ENEMY_RADIUS = 10
ENEMY_HEIGHT = 0.6
ENEMY_DETECT_RANGE = 220
ENEMY_SENSE_RANGE = 120  # if close they can sense you
ENEMY_INSTANT_CHANCE = 0.25  # 25% chance to instantly find you if sensed

def can_see_player(enemy_x, enemy_y, player_x, player_y, game_map, tile_size, map_size):
    dx = player_x - enemy_x
    dy = player_y - enemy_y
    dist = (dx*dx + dy*dy) ** 0.5
    if dist > ENEMY_SENSE_RANGE:
        return False
    ang = math.atan2(dy, dx)
    # quick ray check
    for step in range(1, int(dist)):
        tx = enemy_x + math.cos(ang) * step
        ty = enemy_y + math.sin(ang) * step
        col = int(tx // tile_size)
        row = int(ty // tile_size)
        if not (0 <= col < map_size and 0 <= row < map_size):
            return False
        if game_map[row][col] == 1:
            return False
    return True
import math

