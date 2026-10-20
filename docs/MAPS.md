# Custom Maps Guide

Making maps is designed to be as easy as possible.

## Quick way (recommended)

Edit `maps/custom_maps.py`:

```python
from map_manager import register_map

def load(MAPS, register_map_fn=None):
    reg = register_map_fn or register_map
    reg('arena', 'My Arena', [
        "###########",
        "#S........#",
        "#.#####...#",
        "#.........#",
        "###########",
    ])
```

Save and run - it'll appear in TAB menu.

## Legend
- `#` = Wall
- `.` = Floor (walkable)
- `S` = Player start (required, exactly one)
- space or `o` also work as floor

## Rules
1. Every row must be the same length
2. Surround with `#` border (prevents walking outside)
3. Keep it reasonable size (5x5 up to ~64x64 works fine)
4. Put `S` somewhere open

## Tips
- You can make hallways, rooms, mazes
- Bigger maps work but rendering is fine
- Test in split/full/3D view with `M`
- Want to set as default? Change `ACTIVE_MAP` in `config.py`
