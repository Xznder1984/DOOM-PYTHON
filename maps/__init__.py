"""
CUSTOM MAPS - Add your maps here!
==================================
Just call register_map() with a key, display name, and ASCII text.

Example:
    register_map('my_level', 'My Awesome Level', [
        "##########",
        "#S......#",
        "#.####..#",
        "#......#",
        "##########",
    ])

Legend: # = wall, . = floor, S = start, o or space also count as floor
"""

from map_manager import register_map


def load(MAPS, register_map_fn=None):
    reg = register_map_fn or register_map
    # Add your custom maps below!
    # reg('cool_level', 'Cool Level', [...])
    pass
