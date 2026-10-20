"""
BULLETS - visible tracers
"""
import math

import pygame


class BulletTracer:
    def __init__(self):
        self.tracers = []

    def fire(self, player_x, player_y, player_angle):
        # add a tracer that fades quickly
        self.tracers.append({
            'x1': player_x + math.cos(player_angle) * 5,
            'y1': player_y + math.sin(player_angle) * 5,
            'x2': player_x + math.cos(player_angle) * 80,
            'y2': player_y + math.sin(player_angle) * 80,
            'life': 0.08,
            'born': pygame.time.get_ticks() / 1000.0,
        })

    def update(self, now):
        self.tracers = [t for t in self.tracers if now - t['born'] < t['life']]

    def draw(self, screen, player_x, player_y, player_angle, view_x, view_width):
        # draw simple tracer in middle of screen area
        if not self.tracers:
            return
        h = screen.get_height()
        cx = view_x + view_width // 2
        cy = h // 2 + 20
        for t in self.tracers:
            pygame.draw.line(screen, (255, 230, 150), (cx, cy), (cx + 40, cy - 30), 2)
            pygame.draw.circle(screen, (255, 255, 200), (cx + 40, cy - 30), 3)
