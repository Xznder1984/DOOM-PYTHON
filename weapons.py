"""
WEAPONS & AMMO
==============
Pick from 4 guns, cycle weapons, pick up ammo.

All values live in config.py and here for easy customization.
"""

import math

import pygame

import config


class Weapon:
    def __init__(self, key, data):
        self.key = key
        self.name = data["name"]
        self.damage = data["damage"]
        self.fire_rate = data["fire_rate"]  # seconds between shots
        self.ammo_type = data["ammo_type"]
        self.max_ammo = data.get("max_ammo", 999)
        self.mag_size = data.get("mag_size", 0)  # 0 = no mag, just use ammo pool
        self.bullet_count = data.get("bullet_count", 1)
        self.spread = data.get("spread", 0.0)
        self.auto = data.get("auto", False)
        self.color = data.get("color", (255, 255, 255))
        self.last_shot = 0.0


class WeaponSystem:
    def __init__(self):
        self.weapons = []
        for key in config.WEAPONS_ORDER:
            if key in config.WEAPONS:
                self.weapons.append(Weapon(key, config.WEAPONS[key]))
        self.current = 0
        # ammo pools
        self.ammo = dict(config.STARTING_AMMO)
        # per-weapon state
        self.mag = {}
        for w in self.weapons:
            if w.mag_size > 0:
                self.mag[w.key] = w.mag_size
            else:
                self.mag[w.key] = 0

    def current_weapon(self):
        if not self.weapons:
            return None
        return self.weapons[self.current]

    def next_weapon(self):
        if not self.weapons:
            return
        self.current = (self.current + 1) % len(self.weapons)

    def prev_weapon(self):
        if not self.weapons:
            return
        self.current = (self.current - 1) % len(self.weapons)

    def select(self, index):
        if 0 <= index < len(self.weapons):
            self.current = index

    def can_fire(self, now):
        w = self.current_weapon()
        if not w:
            return False
        if now - w.last_shot < w.fire_rate:
            return False
        # check ammo
        if w.mag_size > 0:
            if self.mag.get(w.key, 0) <= 0:
                # try to reload if possible
                return False
        else:
            if self.ammo.get(w.ammo_type, 0) <= 0 and w.ammo_type != "infinite":
                return False
        return True

    def fire(self, now):
        w = self.current_weapon()
        if not w or not self.can_fire(now):
            return []
        w.last_shot = now
        shots = []
        for i in range(w.bullet_count):
            angle_offset = (pygame.time.get_ticks() / 1000.0) * 0
            # simple spread
            ang = (i - (w.bullet_count - 1) / 2) * w.spread
            shots.append((w.key, w.damage, ang))
        # consume ammo
        if w.mag_size > 0:
            self.mag[w.key] = max(0, self.mag.get(w.key, 0) - 1)
        else:
            if w.ammo_type != "infinite":
                self.ammo[w.ammo_type] = max(0, self.ammo.get(w.ammo_type, 0) - 1)
        return shots

    def reload(self):
        w = self.current_weapon()
        if not w or w.mag_size <= 0:
            return
        need = w.mag_size - self.mag.get(w.key, 0)
        if need <= 0:
            return
        have = self.ammo.get(w.ammo_type, 0)
        take = min(need, have)
        if take > 0:
            self.mag[w.key] += take
            self.ammo[w.ammo_type] -= take

    def give_ammo(self, ammo_type, amount):
        self.ammo[ammo_type] = self.ammo.get(ammo_type, 0) + amount

    def draw_hud(self, screen, font):
        w = self.current_weapon()
        if not w:
            return
        # weapon name
        text = font.render(f"[{self.current + 1}] {w.name}", True, (255, 255, 255))
        screen.blit(text, (10, config.SCREEN_HEIGHT - 60))
        # ammo
        if w.mag_size > 0:
            ammo_text = font.render(f"AMMO: {self.mag.get(w.key, 0)} / {self.ammo.get(w.ammo_type, 0)}", True, (255, 200, 0))
        elif w.ammo_type == "infinite":
            ammo_text = font.render("AMMO: INF", True, (255, 200, 0))
        else:
            ammo_text = font.render(f"AMMO: {self.ammo.get(w.ammo_type, 0)}", True, (255, 200, 0))
        screen.blit(ammo_text, (10, config.SCREEN_HEIGHT - 30))
        # weapon selector
        y = config.SCREEN_HEIGHT - 90
        for i, wep in enumerate(self.weapons):
            color = (255, 255, 0) if i == self.current else (150, 150, 150)
            t = font.render(f"{i+1}. {wep.name}", True, color)
            screen.blit(t, (10, y))
            y -= 20
