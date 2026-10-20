"""
DOOM - CONFIGURATION
====================
Every setting you might want to tweak lives in this one file.
Change something, save, and run the game again.

The numbers derived from other settings (like HALF_FOV) are at the
bottom - you normally don't need to touch those.
"""

import math

import pygame  # only used for the key names in the CONTROLS section

# ---------------------------------------------------------------------------
# GENERAL
# ---------------------------------------------------------------------------
GAME_TITLE = "DOOM - Python Raycaster"
FPS = 60  # frames per second cap

# ---------------------------------------------------------------------------
# SCREEN
# ---------------------------------------------------------------------------
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
# Layout: left half = 2D minimap, right half = first-person 3D view

# ---------------------------------------------------------------------------
# VIEW MODE (the side-by-side layout)
# ---------------------------------------------------------------------------
# Pick your starting layout here. You can also cycle through all of them
# while playing by pressing the "toggle view" key (see CONTROLS below).
#
# "split" = the original look: 2D map on the left half, 3D view on the right
# "full"  = 3D view fills the whole screen, small map overlay in the corner
# "3d"    = 3D view only, no map at all
VIEW_MODES = ["split", "full", "3d"]
VIEW_MODE = "full"  # default to small map overlay + big raycasting view

# Only used in "full" mode: size of the little map overlay in the top-left
OVERLAY_MINIMAP_SIZE = 160
OVERLAY_MINIMAP_MARGIN = 10
OVERLAY_MINIMAP_ALPHA = 120  # background transparency (0 = invisible, 255 = solid)
OVERLAY_MINIMAP_BORDER_COLOR = (230, 230, 230)

# ---------------------------------------------------------------------------
# MAP  -  E1M1 "Hangar" style level
# ---------------------------------------------------------------------------
# Each row is a line of the level, read left to right.
#   '#' = Wall        (the grey/brown blocks you bump into)
#   '.' = Open floor  (walkable space)
#   'S' = Player start (exactly one of these - it becomes open floor)
#
# This is a 32 x 32 grid shaped after DOOM's first map (E1M1 "Hangar"):
# a small start room, a zig-zag corridor, a big room with a nukage pit,
# a side hall and a short exit corridor. It is NOT a byte-for-byte copy
# of the original - it's a compact level in that same style.
#
# BUILDING YOUR OWN LEVEL:
#   1. Make sure every line is the same length.
#   2. Keep a solid border of '#' all the way around.
#   3. Put exactly one 'S' where you want to spawn.
#   That's it - MAP_SIZE is worked out automatically below.
GAME_MAP_TEXT = [
    "################################",
    "#..............................#",
    "#..S...........................#",
    "#..#...........................#",
    "#..#..#############..###########",
    "#..#..#...........#.....#......#",
    "#..#..#...........#.....#......#",
    "#.....#...........#.....#......#",
    "######.###########.#####.#######",
    "#.....#...........#.....#......#",
    "#.....#...........#.....#......#",
    "#.....#...........#.....#......#",
    "#..###########.#################",
    "#..#.........#.#...............#",
    "#..#.........#.#...............#",
    "#............#.#...............#",
    "#............#.#...............#",
    "#..#.........#.#...............#",
    "#..#.........#.#...............#",
    "#..###########.#################",
    "#.............#...............##",
    "#.............#...............##",
    "###############...............##",
    "#.............#...............##",
    "#.............#...............##",
    "################.###############",
    "#.............#...............##",
    "#.............#...............##",
    "#.............#...............##",
    "#.............#...............##",
    "#..............................#",
    "################################",
]


# The raw text above gets converted into the 0/1 grid the engine uses.
# You never need to edit this part - just the picture above.
_GAME_MAP = [
    [0 if char in ".oS" else 1 for char in row]
    for row in GAME_MAP_TEXT
]
MAP_SIZE = len(_GAME_MAP)                       # number of rows (and columns)
GAME_MAP = _GAME_MAP

# COMPUTED VALUES (from the text map)
# These are set automatically when parsing GAME_MAP_TEXT above.
PLAYER_START_COL = 0
PLAYER_START_ROW = 0
TILE_SIZE = SCREEN_HEIGHT // MAP_SIZE  # map always fills the screen height

# ---------------------------------------------------------------------------
# PLAYER
# ---------------------------------------------------------------------------
# Start position is in world pixels (the map is MAP_SIZE * TILE_SIZE big).
# The top-left corner of the map is (0, 0).
# Computed from the 'S' in GAME_MAP_TEXT so it always stays in the right place.
TILE_SIZE = SCREEN_HEIGHT // MAP_SIZE
PLAYER_START_X = (PLAYER_START_COL + 0.5) * TILE_SIZE
PLAYER_START_Y = (PLAYER_START_ROW + 0.5) * TILE_SIZE
PLAYER_START_ANGLE = 0.0  # in radians (0 = facing right/east)
PLAYER_SPEED = 3.0        # pixels moved per frame
PLAYER_RADIUS = 10        # size of the player "body" used for wall collision (smaller = less stuck, but safer with 4-point checks)

# ---------------------------------------------------------------------------
# MOUSE LOOK
# ---------------------------------------------------------------------------
MOUSE_SENSITIVITY = 0.0025  # radians turned per pixel of mouse movement
                            # higher = faster turning

# ---------------------------------------------------------------------------
# RAYCASTING (3D VIEW)
# ---------------------------------------------------------------------------
FOV = math.pi / 3  # 60-degree Field of View
NUM_RAYS = 120                   # number of vertical slices drawn (more = smoother but slower)
MAX_DEPTH = 800                  # max rendering distance in pixels
WALL_PROJECTION_DISTANCE = 400   # bigger = taller walls

# ---------------------------------------------------------------------------
# CONTROLS
# ---------------------------------------------------------------------------
# Change the key names here (see https://www.pygame.org/docs/ref/key.html)
KEY_FORWARD = pygame.K_w
KEY_BACKWARD = pygame.K_s
KEY_STRAFE_LEFT = pygame.K_a     # slide sideways left
KEY_STRAFE_RIGHT = pygame.K_d    # slide sideways right
KEY_ROTATION_SPEED = 0.05        # arrow-key turning speed (keyboard fallback for the mouse)
KEY_TOGGLE_LAYOUT = pygame.K_m   # cycle through the VIEW_MODES while playing
KEY_SHOOT = pygame.K_SPACE
KEY_NEXT_WEAPON = pygame.K_q
KEY_PREV_WEAPON = pygame.K_e
KEY_RELOAD = pygame.K_r
KEY_WEAPON_1 = pygame.K_1
KEY_WEAPON_2 = pygame.K_2
KEY_WEAPON_3 = pygame.K_3
KEY_WEAPON_4 = pygame.K_4
KEY_MAP_MENU = pygame.K_TAB

# ---------------------------------------------------------------------------
# COLORS  (Red, Green, Blue - each 0 to 255)
# ---------------------------------------------------------------------------
BACKGROUND_COLOR = (20, 20, 20)      # behind the minimap
SKY_COLOR = (100, 149, 237)          # cornflower blue
FLOOR_COLOR = (34, 139, 34)          # forest green
MINIMAP_WALL_COLOR = (200, 200, 200)
MINIMAP_FLOOR_COLOR = (0, 0, 0)
PLAYER_COLOR = (255, 0, 0)           # player dot on the minimap
PLAYER_DOT_RADIUS = 8
RAY_COLOR = (255, 255, 0)            # yellow ray lines on the minimap

# ---------------------------------------------------------------------------
# WEAPONS
# ---------------------------------------------------------------------------
# Edit this to add/remove guns. Keep it simple to understand.
WEAPONS_ORDER = ["pistol", "shotgun", "chaingun", "plasma"]
WEAPONS = {
    "pistol": {
        "name": "Pistol",
        "damage": 18,
        "fire_rate": 0.25,
        "ammo_type": "bullets",
        "mag_size": 10,
        "bullet_count": 1,
        "spread": 0.0,
        "auto": False,
        "color": (200, 200, 210),
    },
    "shotgun": {
        "name": "Shotgun",
        "damage": 8,
        "fire_rate": 0.8,
        "ammo_type": "shells",
        "mag_size": 8,
        "bullet_count": 8,
        "spread": 0.12,
        "auto": False,
        "color": (160, 130, 70),
    },
    "chaingun": {
        "name": "Chaingun",
        "damage": 9,
        "fire_rate": 0.08,
        "ammo_type": "bullets",
        "mag_size": 50,
        "bullet_count": 1,
        "spread": 0.04,
        "auto": True,
        "color": (150, 150, 150),
    },
    "plasma": {
        "name": "Plasma Rifle",
        "damage": 14,
        "fire_rate": 0.12,
        "ammo_type": "cells",
        "mag_size": 40,
        "bullet_count": 1,
        "spread": 0.01,
        "auto": True,
        "color": (80, 160, 255),
    },
}
STARTING_AMMO = {
    "bullets": 40,
    "shells": 16,
    "cells": 40,
}

# ---------------------------------------------------------------------------
# MAP SELECTION (easy to add custom maps)
# ---------------------------------------------------------------------------
# Add your own maps in maps/custom_maps.py or just drop entries here.
# Each map needs: name, text (list of strings), or grid + start.
ACTIVE_MAP = "e1m1"

# ---------------------------------------------------------------------------
# DERIVED VALUES (calculated from the settings above - usually no need to edit)
# ---------------------------------------------------------------------------
HALF_WIDTH = SCREEN_WIDTH // 2
HALF_FOV = FOV / 2
STEP_ANGLE = FOV / NUM_RAYS
# (the width of one 3D wall slice is calculated in main.py, because it
#  depends on which VIEW_MODE is active)
