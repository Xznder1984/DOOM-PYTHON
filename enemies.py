"""
ENEMIES - Pac-Man style ghosts
==============================
Keep all enemy settings here so they're easy to tweak.
"""

# Colors per ghost (classic Pac-Man ghost colors)
ENEMY_TYPES = {
    "blinky": {"color": (255, 0, 0), "name": "Blinky", "speed": 1.4, "chase_chance": 0.7},
    "pinky":  {"color": (255, 184, 255), "name": "Pinky",  "speed": 1.3, "chase_chance": 0.6},
    "inky":   {"color": (0, 255, 255), "name": "Inky",   "speed": 1.35, "chase_chance": 0.55},
    "clyde":  {"color": (255, 184, 82), "name": "Clyde",  "speed": 1.25, "chase_chance": 0.5},
}

# Where ghosts start (in world pixels). We'll auto-place them if not set.
# They need to be on open floor tiles.
ENEMY_STARTS = [
    # (x, y, type_key)
    (420.0, 180.0, "blinky"),
    (480.0, 180.0, "pinky"),
    (420.0, 240.0, "inky"),
    (480.0, 240.0, "clyde"),
]

# How big ghosts appear in the world (used for collision/distance)
ENEMY_RADIUS = 12
ENEMY_HEIGHT = 0.6  # sprite height relative to wall height
ENEMY_DETECT_RANGE = 400
