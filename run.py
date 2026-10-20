"""
DOOM - START HERE
=================
This is the file you run:

    python run.py

It runs the game directly - no second process, no launcher window.
Pressing ALT+F4 / the window X / or QUIT in the menu closes it normally.

It also checks pygame is installed and gives a clear message if it isn't,
instead of a scary traceback.

Other files (you don't need to run these):
    main.py           - the game loop and the 3D renderer
    main_menu.py      - the title screen
    mouse_control.py  - mouse look
    config.py         - every setting: map, colors, speed, keys
"""

import sys

# --- Make sure pygame is available before anything else happens ------------
try:
    import pygame
except ImportError:
    print("pygame is not installed for this python:")
    print("   ", sys.executable)
    print()
    print("Fix it with:")
    print("   python -m pip install pygame-ce")
    sys.exit(1)

# --- Run the game ----------------------------------------------------------
import main

if __name__ == "__main__":
    main.main()
