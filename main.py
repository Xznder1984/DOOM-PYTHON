"""
DOOM - Python Raycaster (updated)
==================================
- Default view: big raycasting + small map overlay (press M to cycle)
- 4 guns + ammo, pick with 1-4 or Q/E, shoot with SPACE/Left click
- Pac-Man style ghosts
- Easy custom maps + map selector (TAB)
- Separated into: config.py, map_manager.py, weapons.py, gun_sprites.py,
  enemies.py, sprites.py, mouse_control.py, main_menu.py
"""

import math
import random
import sys

import pygame

import config
from ammo import AMMO_TYPES, place_ammo_random, draw_ammo_on_minimap, draw_ammo_pickups_3d
from bullets import BulletTracer
from enemies import ENEMY_TYPES, ENEMY_STARTS, ENEMY_RADIUS, ENEMY_HEIGHT, ENEMY_DETECT_RANGE
from gun_sprites import GunSprite
from main_menu import MainMenu
from map_manager import get_map
from map_select_menu import MapSelectMenu
from mouse_control import MouseControl
from sprites import draw_ghost_surface
from weapons import WeaponSystem


# ---------------------------------------------------------------------------
# COLLISION
# ---------------------------------------------------------------------------
def is_wall(x, y, game_map, tile_size, map_size):
    col = int(x // tile_size)
    row = int(y // tile_size)
    if not (0 <= col < map_size and 0 <= row < map_size):
        return True
    return game_map[row][col] == 1


def point_inside_wall(x, y, game_map, tile_size, map_size):
    col = int(x // tile_size)
    row = int(y // tile_size)
    if not (0 <= col < map_size and 0 <= row < map_size):
        return True
    return game_map[row][col] == 1


def collides(x, y, game_map, tile_size, map_size, radius):
    r = radius
    # check multiple points for better collision
    for ox in (-r, -r*0.7, 0, r*0.7, r):
        for oy in (-r, -r*0.7, 0, r*0.7, r):
            if ox == 0 and oy == 0:
                continue
            if is_wall(x + ox, y + oy, game_map, tile_size, map_size):
                return True
    return False


def move_player(x, y, dx, dy, game_map, tile_size, map_size, radius):
    nx, ny = x + dx, y + dy
    if not collides(nx, ny, game_map, tile_size, map_size, radius):
        return nx, ny
    # try axis
    if not collides(x + dx, y, game_map, tile_size, map_size, radius):
        x2 = x + dx; y2 = y
        if not collides(x2, y2, game_map, tile_size, map_size, radius):
            return x2, y2
    if not collides(x, y + dy, game_map, tile_size, map_size, radius):
        x2 = x; y2 = y + dy
        if not collides(x2, y2, game_map, tile_size, map_size, radius):
            return x2, y2
    # try smaller
    for m in (0.7, 0.5, 0.3):
        if not collides(x + dx*m, y, game_map, tile_size, map_size, radius):
            return x + dx*m, y
        if not collides(x, y + dy*m, game_map, tile_size, map_size, radius):
            return x, y + dy*m
    # unstuck
    for step in (4, 2, 1, 0.5):
        for ax, ay in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
            cx, cy = x + ax*step, y + ay*step
            if not collides(cx, cy, game_map, tile_size, map_size, radius):
                return cx, cy
    return x, y


# ---------------------------------------------------------------------------
# RENDERING
# ---------------------------------------------------------------------------
def get_layout(view_mode):
    if view_mode == "split":
        view_x = config.HALF_WIDTH
        view_width = config.HALF_WIDTH
    else:
        view_x = 0
        view_width = config.SCREEN_WIDTH
    slice_width = max(1, view_width // config.NUM_RAYS)
    return view_x, view_width, slice_width


def draw_3d_view(screen, player_x, player_y, player_angle, view_x, view_width, slice_width,
                 game_map, tile_size, map_size):
    half_height = config.SCREEN_HEIGHT // 2
    pygame.draw.rect(screen, config.SKY_COLOR, (view_x, 0, view_width, half_height))
    pygame.draw.rect(screen, config.FLOOR_COLOR, (view_x, half_height, view_width, half_height))
    ray_hits = []
    start_angle = player_angle - config.HALF_FOV
    for ray in range(config.NUM_RAYS):
        ray_angle = start_angle + ray * config.STEP_ANGLE
        for depth in range(1, config.MAX_DEPTH):
            target_x = player_x + math.cos(ray_angle) * depth
            target_y = player_y + math.sin(ray_angle) * depth
            if is_wall(target_x, target_y, game_map, tile_size, map_size):
                depth *= math.cos(ray_angle - player_angle)
                wall_height = min(int((tile_size * config.WALL_PROJECTION_DISTANCE) / (depth + 0.0001)), config.SCREEN_HEIGHT)
                shade = 255 / (1 + depth * depth * 0.0001)
                pygame.draw.rect(screen, (shade, shade, shade),
                                 (view_x + ray * slice_width, half_height - wall_height // 2, slice_width, wall_height))
                ray_hits.append((target_x, target_y, depth, ray_angle))
                break
    return ray_hits


def draw_minimap_overlay(screen, player_x, player_y, ray_hits, game_map, tile_size, map_size, enemies=None, pickups=None):
    world_size = map_size * tile_size
    size = config.OVERLAY_MINIMAP_SIZE
    factor = size / world_size if world_size else 1
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    surface.fill((*config.BACKGROUND_COLOR, config.OVERLAY_MINIMAP_ALPHA))
    tile = tile_size * factor
    for row in range(map_size):
        for col in range(map_size):
            if game_map[row][col] == 1:
                pygame.draw.rect(surface, config.MINIMAP_WALL_COLOR, (col*tile, row*tile, max(tile-1,1), max(tile-1,1)))
    for hit_x, hit_y, depth, ray_angle in ray_hits:
        pygame.draw.line(surface, config.RAY_COLOR, (player_x*factor, player_y*factor), (hit_x*factor, hit_y*factor))
    # enemies
    if enemies:
        for e in enemies:
            if not e.get('alive'):
                continue
            et = ENEMY_TYPES.get(e.get('type'), {'color': (255,0,0)})
            pygame.draw.circle(surface, et['color'], (int(e['x']*factor), int(e['y']*factor)), 2)
    # ammo pickups
    if pickups:
        draw_ammo_on_minimap(surface, pickups, factor, tile_size, map_size)
    pygame.draw.circle(surface, config.PLAYER_COLOR, (int(player_x*factor), int(player_y*factor)), 3)
    margin = config.OVERLAY_MINIMAP_MARGIN
    screen.blit(surface, (margin, margin))
    pygame.draw.rect(screen, config.OVERLAY_MINIMAP_BORDER_COLOR, (margin, margin, size, size), 2)


def draw_minimap(screen, player_x, player_y, ray_hits, game_map, tile_size, map_size, enemies=None, pickups=None):
    for row in range(map_size):
        for col in range(map_size):
            color = config.MINIMAP_WALL_COLOR if game_map[row][col] == 1 else config.MINIMAP_FLOOR_COLOR
            pygame.draw.rect(screen, color, (col*tile_size, row*tile_size, tile_size-2, tile_size-2))
    for hit_x, hit_y, depth, ray_angle in ray_hits:
        pygame.draw.line(screen, config.RAY_COLOR, (player_x, player_y), (hit_x, hit_y))
    if enemies:
        for e in enemies:
            if not e.get('alive'):
                continue
            et = ENEMY_TYPES.get(e.get('type'), {'color': (255,0,0)})
            pygame.draw.circle(screen, et['color'], (int(e['x']), int(e['y'])), 4)
    if pickups:
        for p in pickups:
            if not p.get('alive'):
                continue
            color = AMMO_TYPES.get(p['type'], {"color": (255, 255, 0)})["color"]
            pygame.draw.circle(screen, color, (int(p['x']), int(p['y'])), 4)
            pygame.draw.circle(screen, (255,255,255), (int(p['x']), int(p['y'])), 4, 1)
    pygame.draw.circle(screen, config.PLAYER_COLOR, (int(player_x), int(player_y)), config.PLAYER_DOT_RADIUS)


def draw_enemies(screen, player_x, player_y, player_angle, enemies, view_x, view_width, slice_width,
                 game_map, tile_size, map_size):
    # simple sprite projection - draw even if behind walls? requested to see ghost through wall
    half_height = config.SCREEN_HEIGHT // 2
    draw_list = []
    for enemy in enemies:
        if not enemy.get('alive', True):
            continue
        dx = enemy['x'] - player_x
        dy = enemy['y'] - player_y
        dist = math.hypot(dx, dy)
        if dist < 0.1:
            continue
        angle = math.atan2(dy, dx)
        ang_diff = angle - player_angle
        while ang_diff < -math.pi:
            ang_diff += 2*math.pi
        while ang_diff > math.pi:
            ang_diff -= 2*math.pi
        if abs(ang_diff) > config.HALF_FOV * 1.4:
            continue
        dist_corrected = dist * math.cos(ang_diff)
        sprite_height = int((tile_size * config.WALL_PROJECTION_DISTANCE) / (dist_corrected + 0.0001) * ENEMY_HEIGHT)
        sprite_width = sprite_height
        screen_x = view_x + (0.5 + ang_diff/config.FOV) * view_width - sprite_width // 2
        screen_y = half_height - sprite_height // 2
        surf = enemy.get('surf')
        if surf:
            draw_list.append((dist_corrected, screen_x, screen_y, sprite_width, sprite_height, surf))
    draw_list.sort(reverse=True)
    for dist_c, screen_x, screen_y, sprite_width, sprite_height, surf in draw_list:
        scaled = pygame.transform.scale(surf, (int(sprite_width), int(sprite_height)))
        screen.blit(scaled, (int(screen_x), int(screen_y)))


# ---------------------------------------------------------------------------
# GAME
# ---------------------------------------------------------------------------
def game(screen, clock, map_key=None):
    m = get_map(map_key or config.ACTIVE_MAP)
    game_map = [list(row) for row in m['grid']]
    map_size = m['size']
    tile_size = config.SCREEN_HEIGHT // map_size
    # find start
    sc, sr = m['start_col'], m['start_row']
    player_x = (sc + 0.5) * tile_size
    player_y = (sr + 0.5) * tile_size
    player_angle = 0.0
    health = 100

    mouse = MouseControl(config.MOUSE_SENSITIVITY)
    mouse.enable()

    weapons = WeaponSystem()
    gun = GunSprite(screen)
    tracer = BulletTracer()
    font = pygame.font.SysFont('consolas', 16)
    font_big = pygame.font.SysFont('consolas', 22, bold=True)

    # build enemies
    enemies = []
    ghost_surfs = {k: draw_ghost_surface(v['color']) for k,v in ENEMY_TYPES.items()}
    # place ghosts
    for ex, ey, etype in ENEMY_STARTS:
        # make sure not stuck in wall
        if not collides(ex, ey, game_map, tile_size, map_size, ENEMY_RADIUS):
            enemies.append({'x': ex, 'y': ey, 'type': etype, 'hp': 50, 'alive': True, 'surf': ghost_surfs.get(etype)})
    # if none placed (map different), try to scatter
    if not enemies:
        import random
        for _ in range(4):
            for _ in range(100):
                rx = random.randint(2, map_size-2) * tile_size + tile_size/2
                ry = random.randint(2, map_size-2) * tile_size + tile_size/2
                if not collides(rx, ry, game_map, tile_size, map_size, ENEMY_RADIUS):
                    etype = random.choice(list(ENEMY_TYPES.keys()))
                    enemies.append({'x': rx, 'y': ry, 'type': etype, 'hp': 50, 'alive': True, 'surf': ghost_surfs.get(etype)})
                    break

    # ammo pickups
    pickups = place_ammo_random(game_map, tile_size, map_size, count=15)

    view_index = config.VIEW_MODES.index(config.VIEW_MODE)
    firing = False

    while True:
        dt = clock.tick(config.FPS) / 1000.0
        now = pygame.time.get_ticks() / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if mouse.enabled:
                        mouse.disable()
                    else:
                        return "menu"
                if event.key == config.KEY_TOGGLE_LAYOUT:
                    view_index = (view_index + 1) % len(config.VIEW_MODES)
                if event.key == config.KEY_NEXT_WEAPON:
                    weapons.next_weapon()
                if event.key == config.KEY_PREV_WEAPON:
                    weapons.prev_weapon()
                if event.key == config.KEY_RELOAD:
                    weapons.reload()
                if event.key == config.KEY_WEAPON_1:
                    weapons.select(0)
                if event.key == config.KEY_WEAPON_2:
                    weapons.select(1)
                if event.key == config.KEY_WEAPON_3:
                    weapons.select(2)
                if event.key == config.KEY_WEAPON_4:
                    weapons.select(3)
                if event.key == pygame.K_TAB:
                    return "mapselect"
            if event.type == pygame.MOUSEBUTTONDOWN and not mouse.enabled:
                mouse.enable()
            if event.type == pygame.WINDOWFOCUSLOST:
                mouse.disable()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_angle -= config.KEY_ROTATION_SPEED
        if keys[pygame.K_RIGHT]:
            player_angle += config.KEY_ROTATION_SPEED

        speed = config.PLAYER_SPEED
        dx = dy = 0.0
        if keys[config.KEY_FORWARD]:
            dx += math.cos(player_angle) * speed
            dy += math.sin(player_angle) * speed
        if keys[config.KEY_BACKWARD]:
            dx -= math.cos(player_angle) * speed
            dy -= math.sin(player_angle) * speed
        if keys[config.KEY_STRAFE_LEFT]:
            dx += math.cos(player_angle - math.pi/2) * speed
            dy += math.sin(player_angle - math.pi/2) * speed
        if keys[config.KEY_STRAFE_RIGHT]:
            dx += math.cos(player_angle + math.pi/2) * speed
            dy += math.sin(player_angle + math.pi/2) * speed
        player_x, player_y = move_player(player_x, player_y, dx, dy, game_map, tile_size, map_size, config.PLAYER_RADIUS)
        player_angle = mouse.update(player_angle)

        # shooting
        firing = keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]
        if firing and weapons.can_fire(now):
            shots = weapons.fire(now)
            tracer.fire(player_x, player_y, player_angle)
            # simple hitscan - damage closest enemy in crosshair, cannot shoot through walls
            best = None
            best_dist = 9999
            for enemy in enemies:
                if not enemy.get('alive'): continue
                edx = enemy['x'] - player_x
                edy = enemy['y'] - player_y
                edist = math.hypot(edx, edy)
                if edist > 600:
                    continue
                eang = math.atan2(edy, edx)
                adiff = eang - player_angle
                while adiff < -math.pi: adiff += 2*math.pi
                while adiff > math.pi: adiff -= 2*math.pi
                if abs(adiff) < 0.18 and edist < best_dist:
                    # check line of sight - raycast to enemy
                    blocked = False
                    for step in range(1, int(edist)):
                        tx = player_x + math.cos(eang) * step
                        ty = player_y + math.sin(eang) * step
                        if is_wall(tx, ty, game_map, tile_size, map_size):
                            blocked = True
                            break
                    if blocked:
                        continue
                    best_dist = edist
                    best = enemy
            if best and shots:
                best['hp'] -= shots[0][1]
                if best['hp'] <= 0:
                    best['alive'] = False

        # ammo pickup
        for p in pickups:
            if not p.get('alive'):
                continue
            if math.hypot(p['x']-player_x, p['y']-player_y) < 20:
                p['alive'] = False
                weapons.give_ammo(p['type'], AMMO_TYPES.get(p['type'], {'amount': 10})['amount'])

        # enemy movement
        try:
            from enemies import can_see_player as _can_see, ENEMY_SENSE_RANGE as _sr, ENEMY_INSTANT_CHANCE as _ic
        except Exception:
            def _can_see(a,b,c,d,e,f,g): return False
            _sr,_ic = 120,0.25
        for enemy in enemies:
            if not enemy.get('alive'): continue
            edx = player_x - enemy['x']
            edy = player_y - enemy['y']
            edist = math.hypot(edx, edy)
            etype = ENEMY_TYPES.get(enemy['type'], {'speed': 1.1})
            chasing = False
            if edist < _sr:
                try:
                    if _can_see(enemy['x'], enemy['y'], player_x, player_y, game_map, tile_size, map_size):
                        chasing = True
                    elif random.random() < _ic:
                        chasing = True
                except Exception:
                    pass
            if chasing and edist > 2:
                ex = enemy['x'] + (edx/edist)*etype['speed']
                ey = enemy['y'] + (edy/edist)*etype['speed']
                if not collides(ex, ey, game_map, tile_size, map_size, ENEMY_RADIUS):
                    enemy['x'], enemy['y'] = ex, ey
            else:
                if '_dir' not in enemy:
                    import random as _r
                    enemy['_dir'] = _r.uniform(0, math.pi*2)
                import random as _r
                if _r.random() < 0.02:
                    enemy['_dir'] = _r.uniform(0, math.pi*2)
                ex = enemy['x'] + math.cos(enemy['_dir']) * (etype['speed'] * 0.6)
                ey = enemy['y'] + math.sin(enemy['_dir']) * (etype['speed'] * 0.6)
                if not collides(ex, ey, game_map, tile_size, map_size, ENEMY_RADIUS):
                    enemy['x'], enemy['y'] = ex, ey
                else:
                    enemy['_dir'] = _r.uniform(0, math.pi*2)
            # hurt player if close
            if edist < 18:
                health -= 0.1
                if health < 0:
                    health = 0

        # draw
        view_mode = config.VIEW_MODES[view_index]
        view_x, view_width, slice_width = get_layout(view_mode)
        screen.fill(config.BACKGROUND_COLOR)
        ray_hits = draw_3d_view(screen, player_x, player_y, player_angle, view_x, view_width, slice_width,
                                game_map, tile_size, map_size)
        draw_enemies(screen, player_x, player_y, player_angle, enemies, view_x, view_width, slice_width,
                     game_map, tile_size, map_size)
        draw_ammo_pickups_3d(screen, player_x, player_y, player_angle, pickups, view_x, view_width,
                             game_map, tile_size, map_size)
        if view_mode == "split":
            draw_minimap(screen, player_x, player_y, ray_hits, game_map, tile_size, map_size, enemies, pickups)
        elif view_mode == "full":
            draw_minimap_overlay(screen, player_x, player_y, ray_hits, game_map, tile_size, map_size, enemies, pickups)
        gun.draw_crosshair()
        w = weapons.current_weapon()
        if w:
            gun.draw_weapon(w.name, None, firing)
        tracer.update(now)
        tracer.draw(screen, player_x, player_y, player_angle, view_x, view_width)
        weapons.draw_hud(screen, font)
        from ui import draw_bar
        draw_bar(screen, 10, config.SCREEN_HEIGHT - 90, 200, 14, health, 100, (220, 40, 40), (40, 40, 40))
        stamina = 100
        draw_bar(screen, 10, config.SCREEN_HEIGHT - 70, 200, 10, stamina, 100, (40, 200, 80), (40, 40, 40))
        # map name
        map_name = font.render(f"MAP: {m['name']}  |  TAB: Map Select  |  M: View", True, (160, 160, 160))
        screen.blit(map_name, (10, 10))
        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption(config.GAME_TITLE)
    clock = pygame.time.Clock()
    menu = MainMenu(screen, clock)
    mapmenu = MapSelectMenu(screen, clock)
    state = "menu"
    current_map = None
    while state != "quit":
        if state == "menu":
            state = menu.run()
        elif state == "play":
            state = game(screen, clock, current_map)
        elif state == "mapselect":
            mk, action = mapmenu.run()
            if action == "play" and mk:
                current_map = mk
                state = "play"
            elif action == "cancel":
                state = "play" if current_map else "menu"
            elif action == "quit":
                state = "quit"
            else:
                state = "menu"
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
