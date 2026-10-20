"""
GUN SPRITES - draw actual gun images facing forward
"""
import os

import pygame


class GunSprite:
    def __init__(self, screen):
        self.screen = screen
        self.gun_images = {}
        self.load_guns()

    def load_guns(self):
        base = os.path.join(os.path.dirname(__file__), "assets", "guns")
        names = {
            "Pistol": "pistol.png",
            "Shotgun": "shotgun.png",
            "Chaingun": "chaingun.png",
            "Plasma Rifle": "plasma.png",
        }
        for name, fname in names.items():
            path = os.path.join(base, fname)
            try:
                img = pygame.image.load(path).convert_alpha()
                self.gun_images[name] = img
            except Exception:
                self.gun_images[name] = None

    def draw_weapon(self, weapon_name, ammo_info, firing=False):
        w = self.screen.get_width()
        h = self.screen.get_height()
        img = self.gun_images.get(weapon_name)
        if img is not None:
            # scale to fit, point forward at bottom middle
            scale = 0.45
            iw, ih = img.get_size()
            nw, nh = int(iw * scale), int(ih * scale)
            scaled = pygame.transform.scale(img, (nw, nh))
            if firing:
                # slight recoil
                scaled = pygame.transform.scale(scaled, (int(nw * 0.98), int(nh * 0.98)))
                nw, nh = scaled.get_size()
            x = (w - nw) // 2
            y = h - nh + 10
            self.screen.blit(scaled, (x, y))
            return
        # fallback
        if weapon_name == "Pistol":
            pygame.draw.rect(self.screen, (90, 90, 100), (w*0.48, h*0.72, w*0.04, h*0.12), border_radius=4)
            pygame.draw.rect(self.screen, (160, 160, 170), (w*0.48, h*0.7, w*0.04, h*0.04), border_radius=3)
        elif weapon_name == "Shotgun":
            pygame.draw.rect(self.screen, (140, 100, 60), (w*0.47, h*0.7, w*0.06, h*0.14), border_radius=6)
        elif weapon_name == "Chaingun":
            pygame.draw.rect(self.screen, (130, 130, 130), (w*0.46, h*0.68, w*0.08, h*0.16), border_radius=8)
        elif weapon_name == "Plasma Rifle":
            pygame.draw.rect(self.screen, (70, 150, 245), (w*0.47, h*0.69, w*0.06, h*0.15), border_radius=10)

    def draw_crosshair(self):
        w = self.screen.get_width()
        h = self.screen.get_height()
        cx, cy = w // 2, h // 2
        pygame.draw.line(self.screen, (255, 255, 255), (cx - 6, cy), (cx + 6, cy), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (cx, cy - 6), (cx, cy + 6), 2)
        pygame.draw.circle(self.screen, (255, 255, 255), (cx, cy), 2, 1)
