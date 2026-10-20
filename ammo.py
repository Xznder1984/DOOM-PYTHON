"""
AMMO PICKUPS
============
Easy to add ammo on the map. Can be placed randomly or manually.
"""
import random

import pygame


AMMO_TYPES = {
    "bullets": {"color": (255, 200, 0), "amount": 10},
    "shells":  {"color": (200, 160, 60), "amount": 8},
    "cells":   {"color": (80, 160, 255), "amount": 20},
}


def place_ammo_random(game_map, tile_size, map_size, count=12):
    pickups = []
    free = []
    for r in range(map_size):
        for c in range(map_size):
            if game_map[r][c] == 0:
                free.append((c, r))
    random.shuffle(free)
    types = list(AMMO_TYPES.keys())
    for i in range(min(count, len(free))):
        c, r = free[i]
        t = random.choice(types)
        pickups.append({
            "x": (c + 0.5) * tile_size,
            "y": (r + 0.5) * tile_size,
            "type": t,
            "alive": True,
        })
    return pickups


def draw_ammo_on_minimap(screen, pickups, factor, tile_size, map_size):
    for p in pickups:
        if not p.get("alive"):
            continue
        color = AMMO_TYPES.get(p["type"], {"color": (255, 255, 0)})["color"]
        pygame.draw.circle(screen, color, (int(p["x"] * factor), int(p["y"] * factor)), 3)
        pygame.draw.circle(screen, (255, 255, 255), (int(p["x"] * factor), int(p["y"] * factor)), 3, 1)


def draw_ammo_pickups_3d(screen, player_x, player_y, player_angle, pickups, view_x, view_width,
                         game_map, tile_size, map_size):
    half_height = config.SCREEN_HEIGHT // 2
    import config
    for p in pickups:
        if not p.get("alive"):
            continue
        dx = p["x"] - player_x
        dy = p["y"] - player_y
        dist = math.hypot(dx, dy)
        if dist > 250 or dist < 0.1:
            continue
        angle = math.atan2(dy, dx)
        ang_diff = angle - player_angle
        while ang_diff < -math.pi:
            ang_diff += 2 * math.pi
        while ang_diff > math.pi:
            ang_diff -= 2 * math.pi
        if abs(ang_diff) > config.HALF_FOV * 0.8:
            continue
        dist_c = dist * math.cos(ang_diff)
        size = int((tile_size * config.WALL_PROJECTION_DISTANCE) / (dist_c + 0.0001) * 0.25)
        screen_x = view_x + (0.5 + ang_diff / config.FOV) * view_width - size // 2
        screen_y = half_height + 20
        color = AMMO_TYPES.get(p["type"], {"color": (255, 255, 0)})["color"]
        pygame.draw.rect(screen, color, (int(screen_x), int(screen_y), size, size))
        pygame.draw.rect(screen, (255, 255, 255), (int(screen_x), int(screen_y), size, size), 1)
