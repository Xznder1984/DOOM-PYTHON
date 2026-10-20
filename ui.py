import pygame


def draw_bar(screen, x, y, w, h, val, maxv, color, bg):
    pct = val / maxv if maxv > 0 else 0
    if pct < 0: pct = 0
    if pct > 1: pct = 1
    pygame.draw.rect(screen, bg, (x, y, w, h), border_radius=4)
    pygame.draw.rect(screen, color, (x, y, w * pct, h), border_radius=4)
    pygame.draw.rect(screen, (255, 255, 255), (x, y, w, h), width=2, border_radius=4)
