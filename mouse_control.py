"""
MOUSE LOOK
==========
Handles all mouse input for the game, kept separate so main.py stays clean.

How it works:
    mouse = MouseControl(sensitivity)
    mouse.enable()                 -> hide cursor, keep it inside the window
    player_angle = mouse.update(player_angle)   -> call once every frame
    mouse.disable()                -> show the cursor again (menus, alt-tab)

Tweak MOUSE_SENSITIVITY in config.py to change how fast you turn.
"""

import pygame


class MouseControl:
    def __init__(self, sensitivity=0.0025):
        # Radians turned per pixel of mouse movement. Higher = faster turning.
        self.sensitivity = sensitivity
        self.enabled = False

    def enable(self):
        """Grab the mouse: hide the cursor and lock it inside the window."""
        pygame.event.set_grab(True)      # cursor can't leave the window
        pygame.mouse.set_visible(False)  # hide the cursor
        pygame.mouse.get_rel()           # forget old movement so we don't snap
        self.enabled = True

    def disable(self):
        """Release the mouse: show the cursor and let it move freely."""
        pygame.event.set_grab(False)
        pygame.mouse.set_visible(True)
        self.enabled = False

    def update(self, current_angle):
        """
        Read how far the mouse moved since the last frame and return the
        new player angle. Call this once per frame.
        """
        # Always drain the movement, even when disabled - otherwise the
        # motion piles up and the view snaps around when re-enabled.
        dx, _dy = pygame.mouse.get_rel()

        if not self.enabled:
            return current_angle

        return current_angle + dx * self.sensitivity
