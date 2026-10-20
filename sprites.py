"""
SPRITES - Enemy sprites (Pac-Man style ghosts) + pickups
=========================================================
"""

import math

import pygame


def draw_ghost_surface(color, size=64):
    """Draw a simple Pac-Man style ghost sprite."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    s = size
    # body
    pygame.draw.ellipse(surf, color, (s*0.1, s*0.15, s*0.8, s*0.7))
    # bottom frills
    for i in range(4):
        x = s*0.1 + i*s*0.2
        pygame.draw.polygon(surf, color, [(x, s*0.75), (x+s*0.1, s*0.9), (x+s*0.2, s*0.75)])
    # eyes
    pygame.draw.circle(surf, (255, 255, 255), (int(s*0.35), int(s*0.4)), int(s*0.12))
    pygame.draw.circle(surf, (255, 255, 255), (int(s*0.65), int(s*0.4)), int(s*0.12))
    pygame.draw.circle(surf, (0, 0, 50), (int(s*0.38), int(s*0.42)), int(s*0.06))
    pygame.draw.circle(surf, (0, 0, 50), (int(s*0.68), int(s*0.42)), int(s*0.06))
    return surf
