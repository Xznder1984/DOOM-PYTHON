# Weapons & Enemies

## Weapons (4 guns)
All in `config.py` under `WEAPONS`. Pick with `1-4` or `Q/E`, shoot with `SPACE`/Left Click, reload with `R`.

| Gun | Type | Notes |
|---|---|---|
| Pistol | Bullets (mag 10) | Reliable starter |
| Shotgun | Shells (mag 8, 8 pellets) | Spread, great up close |
| Chaingun | Bullets (mag 50, auto) | Fast, good for groups |
| Plasma Rifle | Cells (mag 40, auto) | Mid range energy gun |

Edit damage/fire_rate/spread/bullet_count to balance however you want.

## Ammo
Starting ammo in `config.py` under `STARTING_AMMO`. Ammo types: `bullets`, `shells`, `cells`.

## Enemies (Pac-Man style ghosts)
In `enemies.py` - 4 ghosts: Blinky(red), Pinky(pink), Inky(cyan), Clyde(orange). They chase the player when in range. Tweak `ENEMY_STARTS`, `ENEMY_DETECT_RANGE`, speeds in `ENEMY_TYPES`.

Want more enemies? Just add more entries to `ENEMY_STARTS` in `enemies.py`.
