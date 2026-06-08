import pygame
from pygame import Vector2, sprite
import random
from importlib import resources

from coizera import sfx
from coizera import events
from coizera import pubsub
from coizera import game_state
from coizera import items
from coizera import buildings
from coizera import effects
from coizera import long_init_stuff
from coizera import enemies

# Pygame setup
pygame.init()
pygame.font.init()  # Initialize the font system
pygame.mixer.init()
sfx.load_sfx()

font = pygame.font.SysFont("Consolas", 11)  # Small font for subtle labels below icons

# Get display dimensions
info = pygame.display.Info()
W, H = info.current_w - 80, info.current_h - 80
screen = pygame.display.set_mode((W, H), vsync=True, flags=pygame.RESIZABLE)
clock = pygame.time.Clock()
show_inv = False
show_settings = False
visible_sprites = []



# Settings stuff
volume_rect = pygame.Rect(W // 2, H // 2 - 100, 40, 40)
exit_button_size = 200
tebs = 200
cmss = 80.0
clicked = False

game_settings = {"volume": 0.05}
pygame.mixer.music.set_volume(game_settings["volume"])


pygame.mixer.music.load(resources.files("coizera.assets").joinpath("giggle-touch.mp3"))
pygame.mixer.music.play(-1)





# Initialize item assets
long_init_stuff.init_item_images()
long_init_stuff.init_weapons(30, 100)


def draw_item_icon(surface, item_name, x, y, size):
    """Draws scaled item icon assets dynamically onto slots with aspect-ratio fixes."""
    name_lower = item_name.strip().lower()

    # 1. Check standard items dictionary
    if name_lower in long_init_stuff.ITEM_IMAGES:
        img = long_init_stuff.ITEM_IMAGES[name_lower]
        if img.get_width() != size or img.get_height() != size:
            img = pygame.transform.smoothscale(img, (size, size))
        surface.blit(img, (x, y))
        return

    # 2. Search inside the WEAPONS list and crop the bounding rect to prevent stretching distortion
    weapon_data = next(
        (w for w in long_init_stuff.WEAPONS if w["name"] == name_lower), None
    )
    if weapon_data:
        raw_img = weapon_data["image"]

        # Calculate the actual tight bounding box containing pixels (ignoring empty alpha space)
        clip_rect = raw_img.get_bounding_rect()

        if clip_rect.width > 0 and clip_rect.height > 0:
            # Crop out just the weapon graphics
            cropped_surf = pygame.Surface(
                (clip_rect.width, clip_rect.height), pygame.SRCALPHA
            )
            cropped_surf.blit(raw_img, (0, 0), clip_rect)

            # Determine maximum scale factor to maintain proportions inside the slot
            max_dim = max(clip_rect.width, clip_rect.height)
            scale_ratio = size / max_dim

            new_w = int(clip_rect.width * scale_ratio)
            new_h = int(clip_rect.height * scale_ratio)

            # Smoothly scale the cropped graphic proportionally
            scaled_img = pygame.transform.smoothscale(cropped_surf, (new_w, new_h))

            # Center the scaled weapon proportionally inside the destination slot boundaries
            center_x = x + (size - new_w) // 2
            center_y = y + (size - new_h) // 2
            surface.blit(scaled_img, (center_x, center_y))
        else:
            # Fallback if no layout configuration matches
            if raw_img.get_width() != size or raw_img.get_height() != size:
                raw_img = pygame.transform.smoothscale(raw_img, (size, size))
            surface.blit(raw_img, (x, y))


def add_to_inventory(item_name):
    """Finds next available empty index block and populates with crafted element."""
    if item_name in ["Iron Shortsword", "Iron Broadsword", "Pointy Copper"]:
        for index in range(len(game_state.weapons)):
            if game_state.weapons[index] == "empty":
                game_state.weapons[index] = item_name
                return True
    else:
        for index in range(len(game_state.inventory)):
            if game_state.inventory[index] == "empty":
                game_state.inventory[index] = item_name
                return True
    return False


def next_totorial(tutor):
    if tutor not in long_init_stuff.TUTORIAL_TEXTS:
        return
    text = long_init_stuff.TUTORIAL_TEXTS[tutor]
    line_spacing = 25
    rect_size = (len(text) * line_spacing) + 40
    tbs = pygame.Surface((W // 2 + 50, rect_size), pygame.SRCALPHA).convert_alpha()
    # Set the surface transparency
    tbs.set_alpha(100)
    # Draw the rectangles
    pygame.draw.rect(
        tbs,
        (0, 0, 0),
        (0, 0, W // 2 + 50, rect_size),
        border_radius=20,
    )
    screen.blit(tbs, (W // 2 - 50, 0))
    # Load the font
    tutor_font = pygame.font.SysFont("TimesNewRoman", 20)
    # Draw the shadow text
    for index, line in enumerate(text):
        tutor_surf = tutor_font.render(line, True, (0, 0, 0))
        y_pos = 20 + (index * line_spacing)
        screen.blit(tutor_surf, (W // 2 + 1, y_pos + 1))
    # Draw the main text
    for index, line in enumerate(text):
        tutor_surf = tutor_font.render(line, True, (255, 255, 255))
        y_pos = 20 + (index * line_spacing)
        screen.blit(tutor_surf, (W // 2, y_pos))


def settings():
    global running, show_settings, exit_button_size, tebs
    dark_surf = pygame.Surface((W, H), pygame.SRCALPHA)
    pygame.draw.rect(dark_surf, (0, 0, 0, 200), (0, 0, W, H))
    screen.blit(dark_surf, (0, 0))
    settings_font = pygame.font.SysFont("Consolas", 50, True)
    settings_font_surf = settings_font.render("Settings", True, (255, 255, 255))
    screen.blit(
        settings_font_surf, settings_font_surf.get_rect(center=(W // 2, H // 2 - 200))
    )
    pygame.draw.rect(
        screen, (0, 0, 100), (W // 2, H // 2 - 100, 200, 40), border_radius=20
    )
    pygame.draw.rect(screen, (0, 0, 0), (W // 2, H // 2 - 100, 200, 40), 5, 20)
    setting_id_font = pygame.font.SysFont("Consolas", 30, True)
    setting_id_surf = setting_id_font.render("Volume", True, (255, 255, 255))
    screen.blit(
        setting_id_surf, setting_id_surf.get_rect(center=(W // 2 - 100, H // 2 - 80))
    )
    if (
        volume_rect.collidepoint(pygame.mouse.get_pos())
        and pygame.mouse.get_pressed()[0]
    ):
        volume_rect.centerx = pygame.mouse.get_pos()[0]
    if volume_rect.centerx > W // 2 + 200:
        volume_rect.centerx = W // 2 + 200
    elif volume_rect.centerx < W // 2:
        volume_rect.centerx = W // 2
    pygame.draw.circle(screen, (255, 0, 0), volume_rect.center, 25)
    pygame.draw.circle(screen, (255, 255, 0), volume_rect.center, 20)
    game_settings["volume"] = (volume_rect.centerx - (W // 2)) / 200
    pygame.mixer.music.set_volume(game_settings["volume"])

    exit_button_size = exit_button_size + (tebs - exit_button_size) * 0.2
    exit_button = pygame.Rect(0, 0, exit_button_size, exit_button_size)
    exit_button.center = (W // 2, H // 2 + 300)
    pygame.draw.rect(
        screen,
        (200, 200, 100),
        exit_button,
        border_top_left_radius=20,
        border_bottom_right_radius=20,
    )
    pygame.draw.rect(
        screen,
        (150, 150, 50),
        exit_button,
        25,
        border_top_left_radius=20,
        border_bottom_right_radius=20,
    )
    setting_id_surf = setting_id_font.render("Exit", True, (0, 0, 0))

    # Mathematical Centering Fix: blit the text using its centered rect
    exit_text_rect = setting_id_surf.get_rect(center=exit_button.center)
    screen.blit(setting_id_surf, exit_text_rect)

    if exit_button.collidepoint(pygame.mouse.get_pos()):
        tebs = 200
        if pygame.mouse.get_pressed()[0]:
            running = False
    else:
        tebs = 150


def get_pos_offscreen():
    offset = 150

    # Choose one of the 4 outer sides deterministically (0: Left, 1: Right, 2: Top, 3: Bottom)
    side = random.randint(0, 3)

    if side == 0:  # Left boundary
        random_pos = Vector2(-offset, random.randint(-offset, H + offset))
    elif side == 1:  # Right boundary
        random_pos = Vector2(W + offset, random.randint(-offset, H + offset))
    elif side == 2:  # Top boundary
        random_pos = Vector2(random.randint(-offset, W + offset), -offset)
    else:  # Bottom boundary
        random_pos = Vector2(random.randint(-offset, W + offset), H + offset)

    return random_pos


# --- NEW DYNAMIC SPAWNING HELPER ---
def spawn_enemy(pos, zone, enemy=None):
    """Returns a specific concrete enemy subclass based on the current active zone."""
    if enemy is None:
        if zone == "The Outer Realm":
            return enemies.ShadowStalker(pos, zone)
        elif zone == "mine2":
            return enemies.MagmaSlime(pos, zone)
        else:
            # Defaults to overworld Bouncing Slimes for base, forest, and mine1
            return enemies.BouncingSlime(pos, zone)
    else:
        return enemy(pos, zone)


def draw_mouse(mpos):
    # 2. Tell Python to use the global variable, not a temporary local one
    global cmss, clicked

    if pygame.mouse.get_pressed()[0]:
        MCOLOR1 = (0, 200, 200)  # Cyan outline
        MCOLOR2 = (0, 255, 255)  # Cyan fill
        tmss = 240
        if not clicked:
            game_state.effects_group.add(
                effects.Pop(mpos.x, mpos.y, 10, game_state.zone, (255, 127, 0))
            )
        clicked = True
    else:
        MCOLOR1 = (200, 0, 0)  # Red outline
        MCOLOR2 = (255, 0, 0)  # Red fill
        tmss = 300
        clicked = False

    # 3. The lerp will now smoothly build upon the previous frame's value
    cmss = (tmss - cmss) / 2

    # Create a transparent canvas large enough to hold the cursor and its tail
    msurf = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.mouse.set_visible(False)

    # 1. THE OUTLINE SHAPE (Relative to 0, 0)
    outline_points = [
        (0, 0),  # Tip
        (0, 54),  # Bottom-left corner
        (15, 39),  # Inner crook
        (28, 64),  # Bottom-right of tail
        (36, 60),  # Bottom-left of tail
        (23, 35),  # Outer crook
        (38, 35),  # Right wing tip
    ]
    pygame.draw.polygon(msurf, MCOLOR1, outline_points)

    # 2. THE FILL SHAPE (Relative to 0, 0, tucked inside)
    fill_points = [
        (2, 4),  # Tip tucked slightly in
        (2, 48),  # Bottom-left corner
        (15, 35),  # Inner crook
        (26, 58),  # Bottom-right of tail
        (31, 56),  # Bottom-left of tail
        (20, 33),  # Outer crook
        (33, 33),  # Right wing tip
    ]
    pygame.draw.polygon(msurf, MCOLOR2, fill_points)

    # 4. Convert cmss to an integer before scaling (pygame requires integers for dimensions)
    int_size = int(cmss)
    msurf = pygame.transform.scale(msurf, (int_size, int_size))

    # Draw the finished cursor surface onto the main screen at the mouse coordinates
    screen.blit(msurf, mpos)


# Spawning configuration
item_pool = []
item_timer = 0
max_item_timer = 90
tutor = "Learn Controls"
summon_timer = -1

# ELEGANT REDIRECTION HOOK: Links effects.add to our global effects_group
# This lets the enemy do effects.add() while keeping the active list inside items.py!
effects.add = game_state.effects_group.add
game_state.buildings_group.add(buildings.CraftingTable(Vector2(W // 2 - 80, H // 2 - 80)))

# Event Handlers
@pubsub.event_bus.on(events.PLAYER_PICKS_UP_ITEM)
def on_item_pickup(event: events.PlayerPicksUpItem):
    if add_to_inventory(event.item_name):
        sfx.PICKUP.play()
        game_state.total_items = len(game_state.items_group)

@pubsub.event_bus.on(events.SCREEN_SHAKE)
def on_screen_shake(event: events.ScreenShake):
    game_state.screen_shake = max(game_state.screen_shake, event.intensity)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            W, H = event.w, event.h
            # screen = pygame.display.set_mode((W, H), vsync=True, flags=pygame.RESIZABLE)
            volume_rect.center = (W // 2, H // 2 - 100)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and not game_state.player_group.sprite.dead:
                show_inv = not show_inv  # Toggles exactly once per press
            # Toggles settings menu EXACTWA once per key down
            if event.key == pygame.K_ESCAPE and not game_state.player_group.sprite.dead:
                show_settings = not show_settings
    if not show_settings:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            game_state.items_group.empty()
        if keys[pygame.K_t]:
            if tutor == "Learn Controls":
                tutor = "Build Furnace"
            if tutor == "End of Beginning":
                tutor = None

        summon_timer -= 1
        if summon_timer == 0:
            for _ in range(random.randint(7, 15)):
                rand_pos = get_pos_offscreen()
                game_state.enemy_group.add(spawn_enemy(rand_pos, game_state.zone, enemies.ShadowStalker))

        # Fix: Correctly inspect instances inside buildings_group to advance tutorial states!
        has_furnace = any(isinstance(b, buildings.Furnace) for b in game_state.buildings_group)
        has_ladder = any(isinstance(b, buildings.MineLadder) for b in game_state.buildings_group)
        has_anvil = any(isinstance(b, buildings.Anvil) for b in game_state.buildings_group)
        if tutor == "Build Furnace" and has_furnace:
            tutor = "Build Mineladder"
        if tutor == "Build Mineladder" and has_ladder:
            tutor = "Get Tools"
        if tutor == "Get Tools" and "Pickaxe" in game_state.player_group.sprite.pitems:
            tutor = "Build Anvil"
        if tutor == "Build Anvil" and has_anvil:
            tutor = "End of Beginning"

        # --- DYNAMICALLY CHECK FOR AT LEAST ONE ACTIVE WEAPON ---
        has_weapon = any(w != "empty" for w in game_state.weapons)

        # Spawn mechanics over game ticks
        if game_state.zone == "The Outer Realm":
            item_timer += 1
            if item_timer >= max_item_timer:
                # ONLY spawn if player has at least one weapon!
                if has_weapon and random.randint(1, 4) == 2:
                    item_timer = 0
                    if game_state.total_items < 25:
                        # Fixed: Correctly call your spawn_enemy() helper
                        game_state.enemy_group.add(
                            spawn_enemy(
                                Vector2(
                                    random.randint(100, W - 100),
                                    random.randint(100, H - 100),
                                ),
                                game_state.zone,
                            )
                        )
                elif random.randint(1, 100) == 1:
                    if game_state.total_items < 25:
                        game_state.items_group.add(
                            random.choice(item_pool)(
                                Vector2(
                                    random.randint(100, W - 100),
                                    random.randint(100, H - 100),
                                ),
                                game_state.zone,
                            )
                        )
                    game_state.total_items = len(game_state.items_group)
                    item_timer = 0
        else:
            item_timer += 1
            if item_timer >= max_item_timer:
                # Base/forest/mine zone spawns check for weapons as well!
                if has_weapon and random.randint(1, 2) == 1:
                    game_state.enemy_group.add(
                        spawn_enemy(
                            Vector2(
                                random.randint(100, W - 100),
                                random.randint(100, H - 100),
                            ),
                            game_state.zone,
                        )
                    )
                elif game_state.total_items < 25:
                    game_state.items_group.add(
                        random.choice(item_pool)(
                            Vector2(
                                random.randint(100, W - 100),
                                random.randint(100, H - 100),
                            ),
                            game_state.zone,
                        )
                    )
                game_state.total_items = len(game_state.items_group)
                item_timer = 0

        # --- FIXED TRANSITIONS ---
        if game_state.zone == "base" and game_state.player_group.sprite.pos.x > W:
            game_state.player_group.sprite.pos.x = 10
            game_state.zone = "forest"
        elif game_state.zone == "forest" and game_state.player_group.sprite.pos.x < 0:
            game_state.player_group.sprite.pos.x = W - 10
            game_state.zone = "base"
        if not game_state.player_group.sprite.dead:
            game_state.player_group.update()
        if game_state.player_group.sprite.holding is not None:
            game_state.weapon_group.update()
        game_state.items_group.update()
        game_state.enemy_group.update()
        game_state.effects_group.update()

        # --- PASSING enemy_group TO UPDATE HERE ---
        game_state.projectiles_group.update(game_state.enemy_group)

        # Decay screen shake smoothly over frames
        game_state.screen_shake *= 0.9
        if game_state.screen_shake < 0.1:
            game_state.screen_shake = 0.0

        pubsub.event_bus.dispatch()

    # --- FIXED VACUUM COLLECTION COLLISION ---
    hits = sprite.spritecollide(game_state.player_group.sprite, game_state.items_group, False)
    for item in hits:
        if item.zone == game_state.zone and not item.is_collecting:
            if hasattr(item, "tool"):
                if item.tool in game_state.player_group.sprite.pitems:
                    pubsub.event_bus.publish(
                        events.PLAYER_PICKS_UP_ITEM,
                        events.PlayerPicksUpItem(item_name=item.name),
                    )
                    item.collect()  # Smooth vacuum trigger!
            else:
                pubsub.event_bus.publish(
                    events.PLAYER_PICKS_UP_ITEM,
                    events.PlayerPicksUpItem(item_name=item.name),
                )
                item.collect()  # Smooth vacuum trigger!


    # Check player damaged to trigger screen shake
    hits = sprite.spritecollide(game_state.player_group.sprite, game_state.enemy_group, False)
    if hits:
        for e in hits:
            if e.zone == game_state.zone:
                pubsub.event_bus.publish(
                    events.PLAYER_TAKES_DAMAGE, events.PlayerTakesDamage(damage=e.dmg)
                )

    # Core background & pool updates
    if game_state.zone == "base":
        screen.fill((100, 175, 0))
        if tutor == "Build Furnace":
            item_pool = [items.Rock]
        elif tutor == "Build Mineladder":
            item_pool = [items.Stick]
        else:
            item_pool = [items.Stick, items.Rock, items.Grass]
    elif game_state.zone == "mine1":
        screen.fill((75, 75, 75))
        if tutor == "Build Anvil":
            item_pool = [items.Copper, items.Coal]
        else:
            item_pool = [items.Rock, items.Iron, items.Coal, items.Copper]
    elif game_state.zone == "mine2":
        screen.fill((20, 20, 20))
        item_pool = [items.Iron, items.Magmatite]
        if random.randint(1, 120) == 1 and not show_settings:
            game_state.effects_group.add(
                effects.Twinkle(
                    Vector2(random.randint(0, W), random.randint(0, H)),
                    random.randint(5, 10),
                    game_state.zone,
                    (255, random.randint(0, 255), 0),
                )
            )
    elif game_state.zone == "forest":
        screen.fill((0, 100, 0))
        item_pool = [items.Stick, items.Grass, items.Tree]
    elif game_state.zone == "The Outer Realm":
        screen.fill((50, 25, 75))
        # FIXED: Reduced twinkle spawning from 1-in-10 to 1-in-120 to eliminate lag!
        if random.randint(1, 120) == 1 and not show_settings:
            game_state.effects_group.add(
                effects.Twinkle(
                    Vector2(random.randint(0, W), random.randint(0, H)),
                    random.randint(5, 10),
                    game_state.zone,
                    (255, 0, 255),
                )
            )
        item_pool = [items.DarkEssence]

    # Calculate active dynamic screen shake offsets
    if game_state.screen_shake > 0.1:
        shake_x = random.randint(-int(game_state.screen_shake), int(game_state.screen_shake))
        shake_y = random.randint(-int(game_state.screen_shake), int(game_state.screen_shake))
    else:
        shake_x = 0
        shake_y = 0

    # Rendering game world
    for item in game_state.items_group:
        if item.zone == game_state.zone:
            visible_sprites.append(item)
    for e in game_state.enemy_group:
        if e.zone == game_state.zone:
            visible_sprites.append(e)
    for building in game_state.buildings_group:
        if game_state.zone in building.layers:
            visible_sprites.append(building)
    # Include our active effects directly in the depth sorting pool!
    for fx in game_state.effects_group:
        if fx.zone == game_state.zone:
            visible_sprites.append(fx)

    for p in game_state.projectiles_group:
        if p.zone == game_state.zone:
            visible_sprites.append(p)
    visible_sprites.append(game_state.weapon_group.sprite)
    visible_sprites.append(game_state.player_group.sprite)
    visible_sprites.sort(key=lambda sprite: sprite.rect.bottom)

    # Draw the weapon slash trail OVER everything else (shaken!)
    if game_state.player_group.sprite.holding is not None:
        game_state.weapon_group.sprite.draw_trail(screen, shake_x, shake_y)

    for spr in visible_sprites:
        # Offset drawings dynamically by shake coordinates
        shaken_rect = spr.rect.move(shake_x, shake_y)
        screen.blit(spr.image, shaken_rect)

    # Building systems tick checks
    for b in game_state.buildings_group:
        if game_state.zone in b.layers:
            b.update()

    # Draw active menus
    for b in game_state.buildings_group:
        if hasattr(b, "draw_menu"):
            b.draw_menu(screen)

    # Draw the tutorial text here every frame so it stays on top of the background color
    if tutor is not None:
        next_totorial(tutor)

    # Inventory HUD overlays
    if show_inv:
        slot_size = 50
        padding = 5
        rows = 2
        cols = 5
        inv_width = cols * (slot_size + padding) - padding
        inv_height = rows * (slot_size + padding) - padding
        start_x = 25
        start_y = 25
        for r in range(rows):
            for c in range(cols):
                index = r * 5 + c
                x = start_x + c * (slot_size + padding)
                y = start_y + r * (slot_size + padding)
                pygame.draw.rect(
                    screen, (80, 80, 80), (x, y, slot_size, slot_size), border_radius=5
                )
                pygame.draw.rect(
                    screen,
                    (200, 200, 200),
                    (x, y, slot_size, slot_size),
                    2,
                    border_radius=5,
                )
                item_in_slot = game_state.inventory[index]
                if item_in_slot != "empty":
                    draw_item_icon(screen, item_in_slot, x, y, slot_size)
                icon_rect = pygame.Rect(x, y, slot_size, slot_size)
                if (
                    icon_rect.collidepoint(pygame.mouse.get_pos())
                    and pygame.mouse.get_pressed()[0]
                    and pygame.key.get_pressed()[pygame.K_x]
                ):
                    game_state.inventory[index] = "empty"
                    item_in_slot = "empty"
                if item_in_slot != "empty":
                    text_surface = font.render(item_in_slot, True, (240, 240, 240))
                    max_width = slot_size - 6
                    if text_surface.get_width() > max_width:
                        new_width = max_width
                        new_height = max(
                            1,
                            int(
                                text_surface.get_height()
                                * (max_width / text_surface.get_width())
                            ),
                        )
                        text_surface = pygame.transform.smoothscale(
                            text_surface, (new_width, new_height)
                        )
                    text_rect = text_surface.get_rect(
                        centerx=x + slot_size / 2, bottom=y + slot_size - 2
                    )
                    pygame.draw.rect(
                        screen,
                        (40, 40, 40),
                        (x + 2, y + slot_size - 13, slot_size - 4, 11),
                        border_radius=2,
                    )
                    screen.blit(text_surface, text_rect)

    pos1, pos2 = (70, H - 120), (170, H - 80)
    weapon_positions = [pos1, pos2]
    for i, pos in enumerate(weapon_positions):
        # 1. Draw the slot circles
        pygame.draw.circle(screen, (80, 80, 80), pos, 50)
        pygame.draw.circle(screen, (200, 200, 200), pos, 50, 2)
        # 2. Draw the weapon icon if not empty
        current_weapon = game_state.weapons[i]
        if current_weapon != "empty":
            draw_item_icon(screen, current_weapon, pos[0] - 50, pos[1] - 50, 100)
        # 3. Check for Hover + Click + 'X' key press using circular collision
        mouse_pos = pygame.mouse.get_pos()
        distance = pygame.math.Vector2(mouse_pos).distance_to(pos)
        if (
            distance <= 50  # Inside the 50-radius circle
            and pygame.mouse.get_pressed()[0]
            and pygame.key.get_pressed()[pygame.K_x]
        ):
            game_state.weapons[i] = "empty"  # Deletes the weapon

    red_color = min(
        255, max(0, int(255 - (game_state.player_group.sprite.hp * (255 / game_state.player_group.sprite.max_hp))))
    )
    green_color = min(255, max(0, int(game_state.player_group.sprite.hp * (255 / game_state.player_group.sprite.max_hp))))
    pygame.draw.rect(screen, (0, 0, 0), (W - 245, H - 55, 220, 40), border_radius=10)
    pygame.draw.rect(
        screen,
        (red_color, green_color, 0),
        (W - 235, H - 45, max(0, int(game_state.player_group.sprite.hp * 10)), 20),
        border_radius=10,
    )

    # Check player death states
    if game_state.player_group.sprite.dead:
        game_state.player_group.sprite.dead_timer -= 1
        game_state.enemy_group.empty()
        game_state.inventory.clear()
        for _ in range(10):
            game_state.inventory.append("empty")
        # 1. Draw the dark background overlay
        dark_surf = pygame.Surface((W, H), pygame.SRCALPHA)
        pygame.draw.rect(dark_surf, (0, 0, 0, 200), (0, 0, W, H))
        screen.blit(dark_surf, (0, 0))
        # 2. Render and center "You Died!" (Large Text)
        death_font = pygame.font.SysFont("TimesNewRoman", 80, True)
        death_text_surf = death_font.render("You Died!", True, (255, 0, 0))
        death_rect = death_text_surf.get_rect(center=(W // 2, H // 2 - 40))
        screen.blit(death_text_surf, death_rect)
        # 3. Render and center the Penalty text (Smaller Text)
        penalty_font = pygame.font.SysFont("TimesNewRoman", 30, False, True)
        penalty_text_surf = penalty_font.render(
            "Penalties: Lose all items", True, (200, 200, 200)
        )
        penalty_rect = penalty_text_surf.get_rect(center=(W // 2, H // 2 + 50))
        screen.blit(penalty_text_surf, penalty_rect)
        penalty_text_surf = penalty_font.render(
            "Click anywhere on the screen to continue playing.",
            True,
            (200, 200, 200),
        )
        penalty_rect = penalty_text_surf.get_rect(center=(W // 2, H // 2 + 100))
        screen.blit(penalty_text_surf, penalty_rect)
        if pygame.mouse.get_pressed()[0] and game_state.player_group.sprite.dead_timer <= 0:
            game_state.player_group.sprite.hp = game_state.player_group.sprite.max_hp
            game_state.player_group.sprite.target_hp = game_state.player_group.sprite.max_hp
            game_state.player_group.sprite.dead = False
            game_state.zone = "base"
    if show_settings:
        settings()
    if pygame.Rect(20, 20, W - 20, H - 20).collidepoint(pygame.mouse.get_pos()):
        draw_mouse(Vector2(mouse_pos))
    else:
        pygame.mouse.set_visible(True)
    pygame.display.flip()
    visible_sprites.clear()
    clock.tick(60)

pygame.quit()
