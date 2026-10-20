"""
MAP SELECTION MENU
==================
Press TAB in game to open the map selector. Pick a map with UP/DOWN/ENTER.
"""

import pygame

import config
from map_manager import list_maps


class MapSelectMenu:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.SysFont('consolas', 28, bold=True)
        self.font_small = pygame.font.SysFont('consolas', 18)
        self.maps = list_maps()
        self.selected = 0
        self.bg = (15, 15, 18)

    def draw(self):
        self.screen.fill(self.bg)
        title = self.font.render("SELECT MAP", True, (220, 60, 60))
        self.screen.blit(title, title.get_rect(centerx=self.screen.get_width()//2, top=80))
        y = 150
        for i, m in enumerate(self.maps):
            color = (255, 255, 0) if i == self.selected else (200, 200, 200)
            txt = self.font.render(f"{i+1}. {m['name']} ({m['size']}x{m['size']})", True, color)
            self.screen.blit(txt, txt.get_rect(centerx=self.screen.get_width()//2, top=y))
            y += 40
        hint = self.font_small.render("UP/DOWN to select  |  ENTER to play  |  ESC to cancel", True, (140, 140, 140))
        self.screen.blit(hint, hint.get_rect(centerx=self.screen.get_width()//2, bottom=self.screen.get_height()-40))

    def run(self):
        self.maps = list_maps()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None, 'quit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None, 'cancel'
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.selected = (self.selected - 1) % len(self.maps)
                    if event.key in (pygame.K_DOWN, pygame.K_s):
                        self.selected = (self.selected + 1) % len(self.maps)
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return self.maps[self.selected]['key'], 'play'
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
