"""
MAIN MENU
=========
The title screen: a big DOOM logo, PLAY and QUIT buttons.

How it works:
    menu = MainMenu(screen, clock)
    choice = menu.run()     -> blocks until the player picks something
                               returns "play" or "quit"

Everything visual (colors, button size, hint text) is at the top of
this file - edit it to restyle the menu.
"""

import pygame

# ---------------------------------------------------------------------------
# MENU STYLING (edit these to make the menu your own)
# ---------------------------------------------------------------------------
BACKGROUND_COLOR = (12, 12, 14)

TITLE = "DOOM"
TITLE_COLOR = (198, 30, 30)
TITLE_FONT_SIZE = 110

BUTTON_COLOR = (35, 35, 40)
BUTTON_HOVER_COLOR = (198, 30, 30)  # color while hovered / selected
BUTTON_TEXT_COLOR = (240, 240, 240)
BUTTON_FONT_SIZE = 34
BUTTON_WIDTH = 320
BUTTON_HEIGHT = 64
BUTTON_GAP = 24        # vertical space between buttons
BUTTONS_TOP = 300      # y position of the first button

HINT_COLOR = (150, 150, 150)
HINT_FONT_SIZE = 20
# The little control summary shown at the bottom of the menu
HINTS = [
    "WASD - move      Mouse - look      Arrow keys - turn",
    "M - change view      ESC - release mouse / back to menu",
]

FONT_NAME = "consolas"  # falls back to pygame's default if not installed


def get_font(size, bold=False):
    """Create a font (uses Consolas, or pygame's built-in font as fallback)."""
    return pygame.font.SysFont(FONT_NAME, size, bold=bold)


# ---------------------------------------------------------------------------
# BUTTON
# ---------------------------------------------------------------------------
class Button:
    def __init__(self, text, action, rect):
        self.text = text
        self.action = action      # the value run() returns when clicked
        self.rect = pygame.Rect(rect)

    def contains(self, position):
        """True if the given (x, y) point is on this button."""
        return self.rect.collidepoint(position)

    def draw(self, screen, font, selected):
        """Draw the button - highlighted when selected/hovered."""
        color = BUTTON_HOVER_COLOR if selected else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, width=3, border_radius=12)

        label = font.render(self.text, True, BUTTON_TEXT_COLOR)
        screen.blit(label, label.get_rect(center=self.rect.center))


# ---------------------------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------------------------
class MainMenu:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.title_font = get_font(TITLE_FONT_SIZE, bold=True)
        self.button_font = get_font(BUTTON_FONT_SIZE, bold=True)
        self.hint_font = get_font(HINT_FONT_SIZE)
        self.buttons = self._create_buttons()

    def _create_buttons(self):
        """Stack the buttons vertically, centered on screen."""
        center_x = pygame.display.get_surface().get_width() // 2
        buttons = []
        for index, (text, action) in enumerate([("PLAY", "play"), ("QUIT", "quit")]):
            top = BUTTONS_TOP + index * (BUTTON_HEIGHT + BUTTON_GAP)
            rect = (center_x - BUTTON_WIDTH // 2, top, BUTTON_WIDTH, BUTTON_HEIGHT)
            buttons.append(Button(text, action, rect))
        return buttons

    def draw(self, selected):
        """Draw the whole menu. `selected` is the index of the highlighted button."""
        self.screen.fill(BACKGROUND_COLOR)

        # Title + a red bar underneath it
        title = self.title_font.render(TITLE, True, TITLE_COLOR)
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(title, title_rect)
        bar = pygame.Rect(0, title_rect.bottom + 12, 320, 5)
        bar.centerx = title_rect.centerx
        pygame.draw.rect(self.screen, TITLE_COLOR, bar)

        # Buttons
        for index, button in enumerate(self.buttons):
            button.draw(self.screen, self.button_font, index == selected)

        # Control hints at the bottom
        for index, hint in enumerate(HINTS):
            text = self.hint_font.render(hint, True, HINT_COLOR)
            pos = (self.screen.get_width() // 2, self.screen.get_height() - 70 + index * 26)
            self.screen.blit(text, text.get_rect(center=pos))

    def run(self):
        """
        Show the menu and wait for the player to pick something.
        Returns "play" or "quit".
        """
        selected = 0

        while True:
            # Let hovering with the mouse update the highlight too
            mouse_pos = pygame.mouse.get_pos()
            for index, button in enumerate(self.buttons):
                if button.contains(mouse_pos):
                    selected = index

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons:
                        if button.contains(event.pos):
                            return button.action

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        selected = (selected - 1) % len(self.buttons)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        selected = (selected + 1) % len(self.buttons)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return self.buttons[selected].action

            self.draw(selected)
            pygame.display.flip()
            self.clock.tick(60)
