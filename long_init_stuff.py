import pygame

# Dictionary to hold our item pictures
ITEM_IMAGES = {}
# Unified list of weapon dictionaries containing drawing assets, damage, and effects
WEAPONS = []


def init_item_images():
    """Creates and draws simple 50x50 pixel graphics for each item once at game startup."""
    size = 50

    # --- STICK ---
    stick_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.line(stick_surf, (0, 0, 0), (25, 10), (25, 40), 6)
    # Side branch outline
    pygame.draw.line(stick_surf, (0, 0, 0), (25, 22), (37, 15), 5)

    # 4. Draw the Brown Inner Fill over the outline
    # Main stick fill
    pygame.draw.line(stick_surf, ("brown"), (25, 11), (25, 39), 3)
    # Side branch fill
    pygame.draw.line(stick_surf, ("brown"), (25, 22), (36, 16), 2)
    ITEM_IMAGES["stick"] = stick_surf

    # --- ROCK ---
    rock_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.polygon(
        rock_surf, (120, 120, 120), [(15, 35), (25, 15), (40, 25), (35, 40), (20, 40)]
    )
    pygame.draw.polygon(
        rock_surf, (50, 50, 50), [(15, 35), (25, 15), (40, 25), (35, 40), (20, 40)], 2
    )
    ITEM_IMAGES["rock"] = rock_surf

    # --- SHARP STICK ---
    sharp_stick_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.polygon(sharp_stick_surf, (150, 75, 0), [(10, 35), (15, 45), (40, 10)])
    pygame.draw.polygon(sharp_stick_surf, (0, 0, 0), [(10, 35), (15, 45), (40, 10)], 2)
    ITEM_IMAGES["sharp stick"] = sharp_stick_surf

    # --- GRASS ---
    grass_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.polygon(
        grass_surf, (34, 139, 34), [(10, 40), (15, 15), (23, 28), (32, 10), (40, 40)]
    )
    pygame.draw.polygon(
        grass_surf, (20, 100, 20), [(10, 40), (15, 15), (23, 28), (32, 10), (40, 40)], 2
    )
    ITEM_IMAGES["grass"] = grass_surf

    # --- PICKAXE ---
    pick_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.polygon(pick_surf, (150, 75, 0), [(10, 35), (15, 45), (40, 10)])
    pygame.draw.polygon(pick_surf, (0, 0, 0), [(10, 35), (15, 45), (40, 10)], 2)
    pygame.draw.polygon(
        pick_surf, (127, 127, 127), [(35, 15), (10, 10), (30, 20), (35, 35)]
    )
    pygame.draw.polygon(
        pick_surf, (0, 0, 0), [(35, 15), (10, 10), (30, 20), (35, 35)], 2
    )
    ITEM_IMAGES["pickaxe"] = pick_surf

    # --- IRON ---
    iron_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.polygon(
        iron_surf, (255, 100, 50), [(25, 10), (40, 25), (25, 40), (10, 25)]
    )
    pygame.draw.polygon(iron_surf, (255, 150, 75), [(25, 10), (25, 25), (10, 25)])
    pygame.draw.line(iron_surf, (100, 50, 10), (12, 25), (38, 25), 3)
    pygame.draw.line(iron_surf, (100, 50, 10), (25, 12), (25, 38), 3)
    pygame.draw.polygon(
        iron_surf, (100, 50, 10), [(25, 10), (40, 25), (25, 40), (10, 25)], 3
    )
    ITEM_IMAGES["iron"] = iron_surf

    copper_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.polygon(
        copper_surf, (78, 117, 102), [(25, 10), (40, 25), (25, 40), (10, 25)]
    )
    pygame.draw.polygon(copper_surf, (68, 137, 122), [(25, 10), (25, 25), (10, 25)])
    pygame.draw.line(copper_surf, (58, 97, 82), (12, 25), (38, 25), 3)
    pygame.draw.line(copper_surf, (58, 97, 82), (25, 12), (25, 38), 3)
    pygame.draw.polygon(
        copper_surf, (58, 97, 82), [(25, 10), (40, 25), (25, 40), (10, 25)], 3
    )
    ITEM_IMAGES["copper"] = copper_surf

    # --- COAL ---
    coal_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.polygon(
        coal_surf, (20, 20, 20), [(15, 35), (25, 15), (40, 25), (35, 40), (20, 40)]
    )
    pygame.draw.polygon(
        coal_surf, (50, 50, 50), [(15, 35), (25, 15), (40, 25), (35, 40), (20, 40)], 2
    )
    ITEM_IMAGES["coal"] = coal_surf

    # --- IRON INGOT ---
    iron_ingot_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.polygon(
        iron_ingot_surf,
        (210, 100, 50),
        [(25, 40), (10, 40), (10, 25), (25, 10), (40, 10), (40, 25)],
    )
    pygame.draw.rect(iron_ingot_surf, (100, 50, 50), (10, 25, 16, 16), 3)
    pygame.draw.lines(
        iron_ingot_surf,
        (100, 50, 50),
        False,
        [(10, 25), (25, 10), (40, 10), (40, 25), (25, 40)],
        3,
    )
    pygame.draw.line(iron_ingot_surf, (100, 50, 50), (25, 25), (40, 10), 3)
    ITEM_IMAGES["iron ingot"] = iron_ingot_surf

    copper_ingot_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.polygon(
        copper_ingot_surf,
        (78, 117, 102),
        [(25, 40), (10, 40), (10, 25), (25, 10), (40, 10), (40, 25)],
    )
    pygame.draw.rect(copper_ingot_surf, (58, 97, 82), (10, 25, 16, 16), 3)
    pygame.draw.lines(
        copper_ingot_surf,
        (58, 97, 82),
        False,
        [(10, 25), (25, 10), (40, 10), (40, 25), (25, 40)],
        3,
    )
    pygame.draw.line(copper_ingot_surf, (58, 97, 82), (25, 25), (40, 10), 3)
    ITEM_IMAGES["copper ingot"] = copper_ingot_surf

    # --- SHARP IRON ---
    sharp_iron_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.polygon(sharp_iron_surf, (210, 100, 50), [(10, 35), (15, 45), (40, 10)])
    pygame.draw.polygon(
        sharp_iron_surf, (100, 50, 50), [(10, 35), (15, 45), (40, 10)], 2
    )
    ITEM_IMAGES["sharp iron"] = sharp_iron_surf

    iron_rod_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(iron_rod_surf, (100, 50, 50), (26, 10), 7)
    pygame.draw.circle(iron_rod_surf, (100, 50, 50), (26, 40), 7)
    pygame.draw.line(iron_rod_surf, (100, 50, 50), (25, 40), (25, 10), 14)
    pygame.draw.circle(iron_rod_surf, (210, 100, 50), (26, 10), 5)
    pygame.draw.circle(iron_rod_surf, (210, 100, 50), (26, 40), 5)
    pygame.draw.line(iron_rod_surf, (210, 100, 50), (25, 40), (25, 10), 10)

    ITEM_IMAGES["iron rod"] = iron_rod_surf

    log_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    log_surf = pygame.Surface((50, 50), pygame.SRCALPHA)

    # 1. Main log body (Low-quality bark texture)
    pygame.draw.rect(log_surf, (101, 67, 33), (5, 10, 40, 30))

    # 2. End of the log (Wood rings)
    pygame.draw.ellipse(log_surf, (210, 180, 140), (2, 10, 12, 30))
    pygame.draw.ellipse(log_surf, (139, 90, 43), (5, 17, 6, 16))

    # 3. Bark texture lines
    pygame.draw.line(log_surf, (60, 40, 20), (12, 10), (45, 10), 2)
    pygame.draw.line(log_surf, (60, 40, 20), (12, 38), (45, 38), 2)

    # 4. Small cut branch stub
    pygame.draw.rect(log_surf, (101, 67, 33), (22, 4, 8, 7))
    pygame.draw.ellipse(log_surf, (210, 180, 140), (22, 3, 8, 4))

    ITEM_IMAGES["tree log"] = log_surf

    handle_surf = pygame.Surface((50, 50), pygame.SRCALPHA)

    pygame.draw.circle(handle_surf, (100, 50, 50), (26, 10), 3.5)
    pygame.draw.circle(handle_surf, (100, 50, 50), (26, 40), 3.5)
    pygame.draw.line(handle_surf, (100, 50, 50), (25, 40), (25, 10), 7)
    pygame.draw.circle(handle_surf, ("brown"), (26, 10), 2.5)
    pygame.draw.circle(handle_surf, ("brown"), (26, 40), 2.5)
    pygame.draw.line(handle_surf, ("brown"), (25, 40), (25, 10), 5)

    ITEM_IMAGES["handle"] = handle_surf

    plank_surf = pygame.Surface((50, 50), pygame.SRCALPHA)

    pygame.draw.polygon(
        plank_surf, (150, 75, 0), [(10, 35), (15, 45), (45, 15), (35, 10)]
    )
    pygame.draw.polygon(
        plank_surf, (0, 0, 0), [(10, 35), (15, 45), (45, 15), (35, 10)], 2
    )

    ITEM_IMAGES["wood planks"] = plank_surf

    # --- OLD PARTS (BRASS SCREWS, BOLTS, WASHERS) ---
    old_parts_surf = pygame.Surface((size, size), pygame.SRCALPHA)

    # 1. Flat brass washer (lying down)
    pygame.draw.ellipse(old_parts_surf, (0, 0, 0), (8, 28, 18, 12))
    pygame.draw.ellipse(old_parts_surf, (180, 130, 20), (9, 29, 16, 10))
    pygame.draw.ellipse(old_parts_surf, (0, 0, 0), (13, 32, 8, 4))

    # 2. Brass bolt diagonal
    # Shaft outline & fill
    pygame.draw.line(old_parts_surf, (0, 0, 0), (25, 20), (38, 33), 8)
    pygame.draw.line(old_parts_surf, (139, 105, 20), (26, 21), (37, 32), 4)
    # Thread lines
    pygame.draw.line(old_parts_surf, (0, 0, 0), (29, 22), (32, 27), 2)
    pygame.draw.line(old_parts_surf, (0, 0, 0), (33, 26), (36, 31), 2)

    # Bolt Head outline & fill
    bolt_head = [(13, 16), (23, 10), (30, 17), (26, 24), (16, 24)]
    pygame.draw.polygon(old_parts_surf, (0, 0, 0), bolt_head)
    bolt_head_fill = [(14, 17), (22, 11), (28, 17), (25, 23), (17, 23)]
    pygame.draw.polygon(old_parts_surf, (238, 201, 0), bolt_head_fill)

    # 3. Flathead Screw Head
    pygame.draw.ellipse(old_parts_surf, (0, 0, 0), (22, 22, 16, 12))
    pygame.draw.ellipse(old_parts_surf, (205, 155, 29), (23, 23, 14, 10))
    # Screw Slot line
    pygame.draw.line(old_parts_surf, (0, 0, 0), (25, 28), (35, 24), 2)

    ITEM_IMAGES["old parts"] = old_parts_surf

    dark_essence_surf = pygame.Surface((size, size), pygame.SRCALPHA)

    pygame.draw.circle(dark_essence_surf, (0, 0, 0), (25, 25), 20)
    pygame.draw.circle(dark_essence_surf, (100, 0, 175), (25, 25), 20, 5)

    ITEM_IMAGES["darkness"] = dark_essence_surf

    magmatite_surf = pygame.Surface((size, size), pygame.SRCALPHA)

    # 1. Main Diamond Base (Dark, imperfect volcanic metal)
    pygame.draw.polygon(
        magmatite_surf, (100, 45, 48), [(25, 10), (40, 25), (25, 40), (10, 25)]
    )

    # 2. Left-Side Shadow Shading (Gives the bar a 3D metallic crease)
    pygame.draw.polygon(magmatite_surf, (70, 30, 32), [(25, 10), (25, 25), (10, 25)])

    # 3. Trapped Lava Core Lines (Thick orange cross, pulled inward to prevent leakage)
    # Coordinates changed from 12/38 down to 16/34 to insulate the hot magma inside the bar
    pygame.draw.line(
        magmatite_surf, (255, 140, 0), (16, 25), (34, 25), 4
    )  # Horizontal vein
    pygame.draw.line(
        magmatite_surf, (255, 140, 0), (25, 16), (25, 34), 4
    )  # Vertical vein

    # 4. Deep Red Core Highlight (Provides a realistic, uneven hot glow texture)
    pygame.draw.line(magmatite_surf, (255, 0, 0), (18, 25), (32, 25), 2)
    pygame.draw.line(magmatite_surf, (255, 0, 0), (25, 18), (25, 32), 2)

    # 5. Black Outer Border Outline
    pygame.draw.polygon(
        magmatite_surf, (0, 0, 0), [(25, 10), (40, 25), (25, 40), (10, 25)], 3
    )

    ITEM_IMAGES["magmatite"] = magmatite_surf

    # --------------- Weapons ---------------- #

    isssurf = pygame.Surface((size, size), pygame.SRCALPHA)

    pygame.draw.line(isssurf, (100, 50, 50), (25, 40), (25, 10), 7)
    pygame.draw.line(isssurf, ("brown"), (25, 40), (25, 10), 5)
    pygame.draw.polygon(
        isssurf, (210, 100, 50), [(25, 0), (30, 10), (30, 25), (20, 25), (20, 10)]
    )
    pygame.draw.polygon(
        isssurf, (100, 50, 50), [(25, 0), (30, 10), (30, 25), (20, 25), (20, 10)], 2
    )
    pygame.draw.line(isssurf, (100, 50, 50), (15, 25), (35, 25), 7)
    pygame.draw.line(isssurf, ("brown"), (15, 25), (35, 25), 5)

    ITEM_IMAGES["iron shortsword"] = isssurf

    ibssurf = pygame.Surface((size, size), pygame.SRCALPHA)

    pygame.draw.line(ibssurf, (100, 50, 50), (25, 40), (25, 10), 7)
    pygame.draw.line(ibssurf, ("brown"), (25, 40), (25, 10), 5)
    pygame.draw.polygon(
        ibssurf, (210, 100, 50), [(25, 0), (30, 5), (30, 25), (20, 25), (20, 5)]
    )
    pygame.draw.line(ibssurf, (100, 50, 50), (25, 25), (25, 10), 3)
    pygame.draw.polygon(
        ibssurf, (100, 50, 50), [(25, 0), (30, 5), (30, 25), (20, 25), (20, 5)], 2
    )
    pygame.draw.line(ibssurf, (100, 50, 50), (15, 25), (35, 25), 7)
    pygame.draw.line(ibssurf, ("brown"), (15, 25), (35, 25), 5)

    ITEM_IMAGES["iron broadsword"] = ibssurf

    inferno_icon_surf = pygame.Surface((size, size), pygame.SRCALPHA)

    # Assuming 'size' is defined globally (e.g., size = 50)
    inferno_icon_surf = pygame.Surface((size, size), pygame.SRCALPHA)

    # --- COLORS ---
    black = (0, 0, 0)
    glow_yellow = (255, 215, 0)  # Bright outer heated edge
    glow_orange = (255, 69, 0)  # Inner glowing edge gradient
    blade_base = (120, 50, 20)  # Deep volcanic dark-brown core
    hilt_bronze = (150, 90, 40)  # Guard and pommel bronze tint
    hilt_red = (139, 0, 0)  # Inset crimson gem/bar on the guard
    handle_brown = (101, 67, 33)  # Grip color

    # --- 1. HANDLE & GRIP ---
    # Centered at x=25, running from the bottom up to the guard at y=35
    pygame.draw.line(inferno_icon_surf, handle_brown, (25, 35), (25, 48), width=3)

    # --- 2. HILT / GUARD ---
    # Horizontal crossguard shape centered at x=25, height at y=35
    pygame.draw.line(inferno_icon_surf, hilt_bronze, (13, 35), (37, 35), width=4)
    pygame.draw.line(inferno_icon_surf, hilt_red, (16, 35), (34, 35), width=2)
    pygame.draw.line(inferno_icon_surf, black, (13, 35), (37, 35), width=1)

    # --- 3. VERTICAL FLIPPED BLADE LAYERS ---
    # Connected perfectly to the guard at y=35.
    # Left side is now jagged, Right side is now the smooth curve.
    blade_path = [
        (24, 4),  # Sharp Tip (Pointing straight up, slightly off-center for curve flow)
        (31, 8),  # Right curve upper
        (33, 16),  # Right curve mid
        (31, 26),  # Right curve low
        (29, 35),  # Right base (Flushed against the guard)
        (21, 35),  # Left base (Flushed against the guard)
        (23, 28),  # Left jagged valley 1
        (17, 25),  # Left jagged point 1
        (22, 19),  # Left jagged valley 2
        (18, 15),  # Left jagged point 2
        (23, 10),  # Left jagged valley 3
    ]

    # Outer Yellow Glow Layer
    pygame.draw.polygon(inferno_icon_surf, glow_yellow, blade_path)

    # Inner Orange Glow Layer (Contracted safely inward)
    orange_path = [
        (24, 6),
        (30, 9),
        (31, 16),
        (29, 26),
        (28, 34),
        (22, 34),
        (23, 28),
        (19, 25),
        (22, 19),
        (20, 15),
        (23, 11),
    ]
    pygame.draw.polygon(inferno_icon_surf, glow_orange, orange_path)

    # Main Dark Volcanic Core Layer (Shrunk further to isolate inner metal)
    core_path = [
        (24, 8),
        (29, 10),
        (30, 16),
        (28, 26),
        (27, 34),
        (23, 34),
        (24, 28),
        (20, 25),
        (22, 19),
        (21, 15),
        (23, 12),
    ]
    pygame.draw.polygon(inferno_icon_surf, blade_base, core_path)

    # --- 4. BLACK BLADE OUTLINE ---
    pygame.draw.polygon(inferno_icon_surf, black, core_path, width=1)

    # --- 5. REGISTER ICON ---
    ITEM_IMAGES["inferno"] = inferno_icon_surf

    fire_ingot_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.polygon(
        fire_ingot_surf,
        (255, 0, 0),
        [(25, 40), (10, 40), (10, 25), (25, 10), (40, 10), (40, 25)],
    )
    pygame.draw.rect(fire_ingot_surf, (150, 0, 0), (10, 25, 16, 16), 3)
    pygame.draw.lines(
        fire_ingot_surf,
        (150, 0, 0),
        False,
        [(10, 25), (25, 10), (40, 10), (40, 25), (25, 40)],
        3,
    )
    pygame.draw.line(fire_ingot_surf, (150, 0, 0), (25, 25), (40, 10), 3)
    ITEM_IMAGES["fire ingot"] = fire_ingot_surf


def init_weapons(sizex, sizey):
    isssurf = pygame.Surface((sizex, sizey), pygame.SRCALPHA)

    pygame.draw.line(isssurf, (100, 50, 50), (15, 90), (15, 60), 7)
    pygame.draw.line(isssurf, ("brown"), (15, 90), (15, 60), 5)
    pygame.draw.polygon(
        isssurf, (210, 100, 50), [(15, 0), (25, 25), (25, 55), (5, 55), (5, 25)]
    )
    pygame.draw.polygon(
        isssurf, (100, 50, 50), [(15, 0), (25, 25), (25, 55), (5, 55), (5, 25)], 2
    )
    pygame.draw.line(isssurf, (100, 50, 50), (0, 60), (30, 60), 7)
    pygame.draw.line(isssurf, ("brown"), (0, 60), (60, 60), 5)

    # Populates dictionary layout inside the list as requested
    WEAPONS.append(
        {
            "name": "iron shortsword",
            "image": isssurf,
            "dmg": 1.5,
            "special": {},
        }
    )

    ibssurf = pygame.Surface((sizex, sizey), pygame.SRCALPHA)

    pygame.draw.line(ibssurf, (100, 50, 50), (15, 90), (15, 60), 7)
    pygame.draw.line(ibssurf, ("brown"), (15, 90), (15, 60), 5)
    pygame.draw.polygon(
        ibssurf, (210, 100, 50), [(15, 0), (30, 15), (25, 55), (5, 55), (0, 15)]
    )
    pygame.draw.polygon(
        ibssurf, (100, 50, 50), [(15, 0), (30, 15), (25, 55), (5, 55), (0, 15)], 2
    )
    pygame.draw.line(ibssurf, (100, 50, 50), (15, 60), (15, 10))
    pygame.draw.line(ibssurf, (100, 50, 50), (0, 60), (30, 60), 7)
    pygame.draw.line(ibssurf, ("brown"), (0, 60), (60, 60), 5)

    # Populates dictionary layout inside the list as requested
    WEAPONS.append(
        {
            "name": "iron broadsword",
            "image": ibssurf,
            "dmg": 2,
            "special": {},
        }
    )

    pcsurf = pygame.Surface((sizex, sizey), pygame.SRCALPHA)

    # Define your requested colors
    fill_color = (112, 181, 150)
    outline_color = (78, 117, 102)

    # Custom coordinates for a tall, slender blade bending up and to the right
    points = [
        (5, 95),  # Bottom-left base
        (7, 70),  # Lower left curve
        (11, 45),  # Mid left curve
        (25, 5),  # Pointy dagger tip (swept close to the upper right edge)
        (19, 45),  # Mid right curve
        (21, 70),  # Lower right curve
        (25, 95),  # Bottom-right base
    ]

    # Draw the filled curvy interior
    pygame.draw.polygon(pcsurf, fill_color, points)

    # Draw the pixelated outer outline (width=2)
    pygame.draw.polygon(pcsurf, outline_color, points, 2)

    WEAPONS.append(
        {
            "name": "pointy copper",
            "image": pcsurf,
            "dmg": 0.2,
            "special": {"speed": 0.3},
        }
    )

    inferno_surf = pygame.Surface((30, 100), pygame.SRCALPHA)

    # --- COLORS ---
    black = (0, 0, 0)
    glow_yellow = (255, 215, 0)  # Bright outer heated edge
    glow_orange = (255, 69, 0)  # Inner glowing edge gradient
    blade_base = (120, 50, 20)  # Deep volcanic dark-brown core
    hilt_bronze = (150, 90, 40)  # Guard and pommel bronze tint
    hilt_red = (139, 0, 0)  # Inset crimson gem/bar on the guard
    handle_brown = (101, 67, 33)  # Grip color

    # --- 1. HANDLE & GRIP ---
    # Drawn at the very bottom center (x=15) from y=75 to y=98
    pygame.draw.line(inferno_surf, handle_brown, (15, 75), (15, 98), width=4)

    # --- 2. HILT / GUARD ---
    # Trapezoid guard shape centered at x=15, height from y=70 to y=75
    guard_points = [(3, 70), (27, 70), (23, 75), (7, 75)]
    pygame.draw.polygon(inferno_surf, hilt_bronze, guard_points)
    pygame.draw.polygon(inferno_surf, black, guard_points, width=1)

    # Inset crimson bar on the guard
    pygame.draw.polygon(inferno_surf, hilt_red, [(6, 71), (24, 71), (21, 74), (9, 74)])

    # --- 3. VERTICAL FLIPPED BLADE LAYERS (Drawn back-to-front) ---
    # X-coordinates are perfectly mirrored: Left is jagged, Right is smooth curve.
    blade_path = [
        (13, 2),  # Exact top sharp tip (Mirrored offset to the left)
        (20, 8),  # Right curve upper
        (22, 22),  # Right curve mid
        (19, 45),  # Right curve low
        (24, 70),  # Right base at guard
        (6, 70),  # Left base at guard
        (12, 58),  # Left jagged valley 1
        (5, 52),  # Left jagged point 1
        (13, 40),  # Left jagged valley 2
        (7, 32),  # Left jagged point 2
        (14, 18),  # Left jagged valley 3
    ]

    # Outer Yellow Glow Layer
    pygame.draw.polygon(inferno_surf, glow_yellow, blade_path)

    # Inner Orange Glow Layer (Slightly contracted coordinates)
    orange_path = [
        (13, 4),
        (19, 9),
        (21, 22),
        (18, 45),
        (23, 69),
        (7, 69),
        (12, 57),
        (6, 52),
        (13, 41),
        (8, 32),
        (14, 19),
    ]
    pygame.draw.polygon(inferno_surf, glow_orange, orange_path)

    # Main Dark Volcanic Core Layer (Shrunk further inward)
    core_path = [
        (13, 7),
        (18, 11),
        (19, 22),
        (17, 45),
        (22, 68),
        (8, 68),
        (12, 56),
        (8, 52),
        (13, 42),
        (9, 32),
        (13, 21),
    ]
    pygame.draw.polygon(inferno_surf, blade_base, core_path)

    # --- 4. BLACK BLADE OUTLINE ---
    pygame.draw.polygon(inferno_surf, black, core_path, width=1)

    # --- 5. APPEND TO WEAPONS SYSTEM ---
    WEAPONS.append(
        {
            "name": "inferno",
            "image": inferno_surf,
            "dmg": 2.6,
            "special": {"fire": (255, 150, 120), "slow": 0.1},
        }
    )


CRAFTING_RECIPES = {
    "Sharp Stick": {
        "ingredients": {"Stick": 1, "Rock": 1},
        "result": "Sharp Stick",
        "building": "Crafting Table",
    },
    "Mine Ladder": {
        "ingredients": {"Stick": 10},
        "result": "Mine Ladder",
        "building": "Crafting Table",
    },
    "Furnace": {
        "ingredients": {"Rock": 10},
        "result": "Furnace",
        "building": "Crafting Table",
    },
    "Plankings": {
        "ingredients": {"Tree Log": 1},
        "result": "Wood Planks",
        "building": "Crafting Table",
    },
    "Monstah Thing": {
        "ingredients": {"Wood Planks": 2, "Stick": 2, "Sharp Stick": 1},
        "result": "Monstahs",
        "building": "Crafting Table",
    },
    "Weapon Handle": {
        "ingredients": {"Stick": 1, "Grass": 1},
        "result": "Handle",
        "building": "Crafting Table",
    },
    "Pickaxe": {
        "ingredients": {"Stick": 1, "Rock": 2, "Grass": 2},
        "result": "Pickaxe",
        "building": "Crafting Table",
    },
    "Axe": {
        "ingredients": {"Stick": 1, "Rock": 2, "Grass": 2},
        "result": "Axe",
        "building": "Crafting Table",
    },
    "Anvil": {
        "ingredients": {"Copper Ingot": 5},
        "result": "Anvil",
        "building": "Crafting Table",
    },
    "Monster Portal": {
        "ingredients": {"Old Parts": 3, "Iron Rod": 3},
        "result": "Monster Portal",
        "building": "Crafting Table",
    },
    "Iron Ingot": {
        "ingredients": {"Iron": 2},
        "result": "Iron Ingot",
        "building": "Furnace",
    },
    "Copper Ingot": {
        "ingredients": {"Copper": 2},
        "result": "Copper Ingot",
        "building": "Furnace",
    },
    "Fire Ingot": {
        "ingredients": {"Magmatite": 3},
        "result": "Fire Ingot",
        "building": "Furnace",
    },
    "Sharp Iron": {
        "ingredients": {"Sharp Stick": 1, "Iron": 4},
        "result": "Sharp Iron",
        "building": "Furnace",
    },
    "Iron Rod": {
        "ingredients": {"Iron Ingot": 3},
        "result": "Iron Rod",
        "building": "Anvil",
    },
    "Pointy Copper": {
        "ingredients": {"Copper Ingot": 2},
        "result": "Pointy Copper",
        "building": "Anvil",
    },
    "Copper Pickaxe": {
        "ingredients": {"Copper Ingot": 4, "Handle": 1},
        "result": "Copper Pickaxe",
        "building": "Anvil",
    },
    "Iron Pickaxe": {
        "ingredients": {"Iron Rod": 3, "Handle": 1, "Iron Ingot": 2},
        "result": "Iron Pickaxe",
        "building": "Anvil",
    },
    "Iron Shortsword": {
        "ingredients": {"Sharp Iron": 1, "Handle": 1},
        "result": "Iron Shortsword",
        "building": "Anvil",
    },
    "Iron Broadsword": {
        "ingredients": {"Sharp Iron": 1, "Iron Rod": 2, "Handle": 1},
        "result": "Iron Broadsword",
        "building": "Anvil",
    },
    "Void Iron": {
        "ingredients": {"Iron Ingot": 2, "Dark Essence": 2},
        "result": "Void Iron",
        "building": "Anvil",
    },
    "Super Ladder!": {
        "ingredients": {"Iron Rod": 5, "Old Parts": 5},
        "result": "Super Ladder!",
        "building": "Anvil",
    },
    "Inferno": {
        "ingredients": {"Iron Rod": 5, "Fire Ingot": 3, "Handle": 1},
        "result": "Inferno",
        "building": "Anvil",
    },
}

# Tutorial texts organized into a clean dictionary
TUTORIAL_TEXTS = {
    "Learn Controls": [
        "Sup dude! Your going to need to know some stuff before you start your adventure!",
        "If you want to incinerate something in your inventory!",
        "Hover your mouse over the item you want to destroy, click while holding 'x' down!",
        "If none of the items you want are spawning, try pressing 'z' to remove all of them.",
        "To see inside of your inventory, press 'e' to open and close it. The top grid is your items.",
        "And the bottom two circles are where your weapons will go!",
        "To open the crafting table, click on it and a menu will pop up!",
        "To move on to the next tutorial, press 't'!",
    ],
    "Build Furnace": [
        "To start things off, you might wanna build a furnace!",
        "Take a look at the crafting table and look for the recipe.",
        "It should say 'Rock: 10'. That means you need to have 10 rocks",
        "in your inventory to build a Furnace!",
        "Build a furnace to move on to the next tutorial",
    ],
    "Build Mineladder": [
        "Now, you're going to need a mineladder! Building a mineladder is just like building a furnace!",
        "But instead of rocks, you need 10 sticks as shown on the recipe.",
        "Just grab those sticks, click on the recipe and you'll have access to the mine in no time!",
    ],
    "Get Tools": [
        "You'll find that you cant pick up the copper ore, thats because you don't have a pick yet!",
        "To build one, look for the recipe and get the stuff you need.",
        "If you want, go ahead and make an axe too, you'll need it later!",
    ],
    "Build Anvil": [
        "You're just about ready to start your adventure!",
        "There's just one more thing though, you're going to need an anvil to smith stuff!",
        "This is not like any other build you've made before because you first need to make ingots!",
        "To make ingots, you need to grab one coal, and two copper ores and place them in the furnace.",
        "repeat this process 5 times and you will have 5 copper ingots.",
        "use them to make an anvil in the crafting menu!",
    ],
    "End of Beginning": [
        "Hopefully this tutorial was of use to you, thanks for playing Coizera!"
    ],
}
