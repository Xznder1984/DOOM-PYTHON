"""
MAP MANAGER - Easy custom maps
==============================
This file makes it extremely easy to add new maps. You can define maps
here, or in maps/custom_maps.py. Maps are stored as ASCII text (# walls, . floor, S start).
"""

from collections import OrderedDict


def text_to_grid(text_map):
    """Convert ASCII map to 2D grid (1=wall, 0=floor). Return (grid, start_col, start_row)."""
    grid = []
    start_col = start_row = 0
    for r, row in enumerate(text_map):
        g_row = []
        for c, ch in enumerate(row):
            if ch == 'S':
                start_col, start_row = c, r
                g_row.append(0)
            elif ch == '.' or ch == 'o' or ch == ' ':
                g_row.append(0)
            elif ch == '#':
                g_row.append(1)
            else:
                g_row.append(1 if ch == '#' else 0)
        grid.append(g_row)
    return grid, start_col, start_row


MAPS = OrderedDict()


def register_map(key, name, text_map):
    grid, sc, sr = text_to_grid(text_map)
    MAPS[key] = {
        'key': key,
        'name': name,
        'text': text_map,
        'grid': grid,
        'size': len(grid),
        'start_col': sc,
        'start_row': sr,
    }


# Built-in maps
register_map(
    'e1m1',
    'E1M1 - Hangar Style',
    [
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
    ],
)

register_map(
    'corridor',
    'Test Corridor',
    [
        "########################",
        "#S....................#",
        "#..##################..#",
        "#......................#",
        "#..##################..#",
        "#......................#",
        "########################",
    ],
)

register_map(
    'box',
    'Small Arena',
    [
        "############",
        "#S........#",
        "#.######..#",
        "#.#....#..#",
        "#.#.##.#..#",
        "#.#....#..#",
        "#.######..#",
        "#.........#",
        "############",
    ],
)


# Load custom maps if they exist
try:
    from maps import custom_maps  # type: ignore
    custom_maps.load(MAPS, register_map)
except Exception:
    pass


def get_map(key):
    return MAPS.get(key, MAPS[list(MAPS.keys())[0]] if MAPS else None)


def list_maps():
    return list(MAPS.values())
