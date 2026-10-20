"""
GUNS SPRITES / HUD
==================
Draw weapon view model on screen (simple placeholder that looks like a gun).
Also handles crosshair.
"""

import pygame


class GunSprite:
    def __init__(self, screen):
        self.screen = screen

    def draw_weapon(self, weapon_name, ammo_info, firing=False):
        w = self.screen.get_width()
        h = self.screen.get_height()
        # base gun body
        if weapon_name == "Pistol":
            color = (100, 100, 120)
            barrel = (180, 180, 180)
            pygame.draw.rect(self.screen, color, (w * 0.65, h * 0.65, w * 0.15, h * 0.08), border_radius=4)
            pygame.draw.rect(self.screen, barrel, (w * 0.8, h * 0.67, w * 0.08, h * 0.02), border_radius=2)
            pygame.draw.rect(self.screen, (60, 60, 70), (w * 0.65, h * 0.72, w * 0.12, h * 0.06), border_radius=3)
        elif weapon_name == "Shotgun":
            color = (160, 120, 60)
            pygame.draw.rect(self.screen, color, (w * 0.6, h * 0.67, w * 0.25, h * 0.05), border_radius=4)
            pygame.draw.rect(self.screen, (80, 60, 40), (w * 0.6, h * 0.72, w * 0.22, h * 0.05), border_radius=3)
        elif weapon_name == "Chaingun":
            color = (140, 140, 140)
            pygame.draw.rect(self.screen, color, (w * 0.55, h * 0.65, w * 0.25, h * 0.07), border_radius=6)
            pygame.draw.rect(self.screen, (60, 60, 60), (w * 0.55, h * 0.72, w * 0.2, h * 0.08), border_radius=4)
            pygame.draw.rect(self.screen, (180, 180, 180), (w * 0.78, h * 0.66, w * 0.08, h * 0.03), border_radius=2)
        elif weapon_name == "Plasma Rifle":
            color = (80, 160, 255)
            glow = (120, 200, 255)
            pygame.draw.rect(self.screen, color, (w * 0.58, h * 0.66, w * 0.22, h * 0.06), border_radius=8)
            pygame.draw.rect(self.screen, (20, 80, 160), (w * 0.58, h * 0.72, w * 0.18, h * 0.07), border_radius=6)
            if firing:
                pygame.draw.circle(self.screen, glow, (int(w * 0.8), int(h * 0.69)), 6)
            else:
                pygame.draw.circle(self.screen, (40, 100, 200), (int(w * 0.8), int(h * 0.69)), 5)

    def draw_crosshair(self):
        w = self.screen.get_width()
        h = self.screen.get_height()
        cx, cy = w // 2, h // 2
        pygame.draw.line(self.screen, (255, 255, 255), (cx - 8, cy), (cx + 8, cy), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (cx, cy - 8), (cx, cy + 8), 2)
        pygame.draw.circle(self.screen, (255, 255, 255), (cx, cy), 2, 1)
