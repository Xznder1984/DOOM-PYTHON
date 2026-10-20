# DOOM-PYTHON

A tiny, easy-to-hack Doom-style raycaster built with Python + Pygame. Great for learning raycasting, modding maps, and messing with weapons/enemies.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame/Pygame--CE-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

Repo: [https://github.com/Xznder1984/DOOM-PYTHON](https://github.com/Xznder1984/DOOM-PYTHON)

## Features

- **Classic raycasting** - First-person view with walls, sky/floor, fisheye-corrected
- **Default view is just right** - Big raycasting view with a small map overlay (press `M` to cycle: split / full / 3D only)
- **Pac-Man style ghosts** - 4 colored ghosts that wander/chase you
- **4 guns + ammo** - Pistol, Shotgun, Chaingun, Plasma Rifle. Pick with `1-4` or `Q/E`. Reload with `R`. Shoot with `SPACE` or Left Mouse
- **Easy custom maps** - Draw maps in ASCII, add them in seconds
- **Map selector** - Press `TAB` in-game to pick any map
- **Mouse look + WASD movement** - Feels nice and easy to customize
- **Separated files** - Everything is split so it's easy to understand and extend

## Quick Start

```bash
# Install dependencies
pip install pygame-ce

# Run the game
python run.py
```

Or just `python main.py` / `python launch.py` too.

## Controls

| Key | Action |
|---|---|
| `WASD` | Move |
| `Mouse` | Look around |
| `Arrow Keys` | Turn (backup) |
| `SPACE` / `Left Mouse` | Shoot |
| `1-4` or `Q/E` | Switch weapons |
| `R` | Reload |
| `TAB` | Map selector |
| `M` | Cycle view mode |
| `ESC` | Release mouse / Back to menu |

## Project Structure

```
DOOM-PYTHON/
├── run.py           # Start here (auto-handles pygame)
├── main.py          # Game loop, rendering, enemies/guns integration
├── main_menu.py     # Title screen
├── map_manager.py   # Map loading system (easy to extend)
├── map_select_menu.py # In-game map picker
├── maps/
│   ├── __init__.py
│   └── custom_maps.py # ADD YOUR CUSTOM MAPS HERE
├── weapons.py       # Weapon/ammo system
├── gun_sprites.py   # Gun viewmodel + crosshair
├── enemies.py       # Enemy settings
├── sprites.py       # Ghost sprites
├── mouse_control.py # Mouse look
├── config.py        # All settings in one place (guns, colors, etc)
└── docs/            # Documentation
```

## Making Custom Maps (SUPER Easy)

Open `maps/custom_maps.py` and add:

```python
from map_manager import register_map

def load(MAPS, register_map_fn=None):
    reg = register_map_fn or register_map
    reg('my_map', 'My Cool Map', [
        "##########",
        "#S........#",
        "#..####..#",
        "#........#",
        "##########",
    ])
```

Legend: `#` wall, `.` floor, `S` start. Every row same length, keep border walls. That's it - it'll show up in the map selector automatically.

You can also add maps straight in `map_manager.py` if you want. See `docs/MAPS.md` for more details.

## Tweak Everything

Everything is in `config.py` - map, screen size, FOV, colors, weapon stats, enemy behavior, etc. Want to change gun damage? Edit `WEAPONS`. Want different starting ammo? Edit `STARTING_AMMO`. Want to move ghosts? Edit `ENEMY_STARTS` in `enemies.py`.

## Docs

- [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)
- [docs/MAPS.md](docs/MAPS.md)
- [docs/WEAPONS_ENEMIES.md](docs/WEAPONS_ENEMIES.md)
- [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)

## Website

Check out the website in `website/` - a simple human-made page with rate limiting and a custom 404 page. Just open `index.html` locally or host it anywhere.

## License

MIT License - do whatever you want with it!
