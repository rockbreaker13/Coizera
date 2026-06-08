import pygame
from abc import ABC, abstractmethod
import random
import math

from coizera import long_init_stuff
from coizera import effects
from coizera import game_state

# Fonts init
pygame.font.init()
ui_font = pygame.font.SysFont("Consolas", 13)
title_font = pygame.font.SysFont("Consolas", 48)


class Building(pygame.sprite.Sprite, ABC):
    def __init__(self, pos=None):
        super().__init__()
        self.image = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (100, 100, 100), (0, 0, 80, 80), border_radius=10)
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, 80, 80), 5, 10)
        self.rect = self.image.get_rect()

        if pos is not None:
            self.pos = pos
        else:
            self.pos = pygame.Vector2(
                random.randint(100, game_state.W - 100), random.randint(100, game_state.H - 100)
            )

    @abstractmethod
    def update(self):
        self.rect.center = self.pos
        if (
            self.rect.collidepoint(pygame.mouse.get_pos())
            and pygame.mouse.get_pressed()[0]
            and pygame.key.get_pressed()[pygame.K_LCTRL]
        ):
            self.pos = pygame.Vector2(pygame.mouse.get_pos())


class CraftingTable(Building):
    def __init__(self, pos=None, layers=["base"]):
        super().__init__(pos)
        self.recipe_unlocked = True
        self.is_active = False
        self.click_cooldown = 0
        self.layers = layers
        self.crafting_rects = []

        # Dictionary to track the smooth scaling animation for each recipe card
        self.card_scales = {}

        pygame.draw.rect(self.image, (139, 69, 19), (20, 20, 40, 40), border_radius=5)
        pygame.draw.rect(self.image, (0, 0, 0), (20, 20, 40, 40), 3, border_radius=5)
        pygame.draw.line(self.image, (0, 0, 0), (40, 20), (40, 60), 2)
        pygame.draw.line(self.image, (0, 0, 0), (20, 40), (60, 40), 2)

    def update(self):
        super().update()
        if self.click_cooldown > 0:
            self.click_cooldown -= 1

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.is_active = True

        if (
            self.is_active
            and pygame.key.get_pressed()[pygame.K_e]
            or pygame.key.get_pressed()[pygame.K_ESCAPE]
        ):
            self.is_active = False

    def draw_menu(self, screen):
        if not self.is_active:
            return

        inventory = game_state.inventory
        W, H = screen.get_size()

        pygame.draw.rect(screen, (139, 69, 19), (0, 0, W, H))
        pygame.draw.rect(screen, ("brown"), (0, 0, W, H), 10)

        title_surf = title_font.render("Crafting", True, (50, 50, 155))
        title_rect = title_surf.get_rect(center=(W // 2 + 5, H - 95))
        screen.blit(title_surf, title_rect)

        title_surf = title_font.render("Crafting", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(W // 2, H - 100))
        screen.blit(title_surf, title_rect)

        start_x = 150
        start_y = 150
        row_gap = 200
        current_y = start_y
        current_x = start_x

        for r in long_init_stuff.CRAFTING_RECIPES:
            recipe_data = long_init_stuff.CRAFTING_RECIPES[r]

            if recipe_data["building"] == "Crafting Table":
                ingredients_dict = recipe_data["ingredients"]
                card_rect = pygame.Rect(current_x, current_y, 150, 120)

                # Initialize scaling value for this specific card if not already tracked
                if r not in self.card_scales:
                    self.card_scales[r] = 1.0

                mouse_pos = pygame.mouse.get_pos()
                is_hovered = card_rect.collidepoint(mouse_pos)

                # Apply the Target Scale Math (Grow to 1.5 when hovered, sink back to 1.0 when not)
                target_scale = 1.5 if is_hovered else 1.0
                self.card_scales[r] += (target_scale - self.card_scales[r]) * 0.2

                # Create a temporary card surface to draw everything on (sized 130x130 to allow room for the shadow offset)
                card_surf = pygame.Surface((160, 130), pygame.SRCALPHA)

                if recipe_data["result"] not in game_state.player_group.sprite.pitems:
                    pygame.draw.rect(
                        card_surf,
                        ("brown"),
                        (10, 10, 150, 120),
                        border_radius=5,
                    )
                    pygame.draw.rect(
                        card_surf,
                        (100, 100, 100),
                        (0, 30, 150, 90),
                        border_radius=5,
                    )
                    pygame.draw.rect(card_surf, (10, 10, 10), (0, 0, 150, 120), 10, 5)
                else:
                    pygame.draw.rect(
                        card_surf,
                        (50, 50, 50),
                        (10, 10, 150, 120),
                        border_radius=5,
                    )
                    pygame.draw.rect(
                        card_surf,
                        (10, 10, 10),
                        (0, 30, 150, 90),
                        border_radius=5,
                    )
                    pygame.draw.rect(card_surf, (10, 10, 10), (0, 0, 150, 120), 10, 5)

                if is_hovered:
                    if recipe_data["result"] not in game_state.player_group.sprite.pitems:
                        pygame.draw.rect(
                            card_surf, (255, 127, 10), (0, 0, 150, 120), 10, 5
                        )
                        if pygame.mouse.get_pressed()[0] and self.click_cooldown == 0:
                            self.click_cooldown = 15

                            current_counts = {}
                            for item in inventory:
                                if item != "empty":
                                    current_counts[item] = (
                                        current_counts.get(item, 0) + 1
                                    )

                            can_craft = True
                            for ing_name, required_amount in ingredients_dict.items():
                                if current_counts.get(ing_name, 0) < required_amount:
                                    can_craft = False
                                    break

                            if can_craft:
                                for (
                                    ing_name,
                                    required_amount,
                                ) in ingredients_dict.items():
                                    removed = 0
                                    for index in range(len(inventory)):
                                        if inventory[index] == ing_name:
                                            inventory[index] = "empty"
                                            removed += 1
                                            if removed == required_amount:
                                                break

                                if recipe_data["result"] in [
                                    "Mine Ladder",
                                    "Furnace",
                                    "Anvil",
                                    "Monster Portal",
                                ]:
                                    random_x = random.randint(100, game_state.W - 100)
                                    random_y = random.randint(100, game_state.H - 100)
                                    spawn_pos = pygame.Vector2(random_x, random_y)

                                    if recipe_data["result"] == "Mine Ladder":
                                        new_building = MineLadder(spawn_pos)
                                        game_state.buildings_group.add(new_building)
                                    elif recipe_data["result"] == "Furnace":
                                        new_building = Furnace(spawn_pos)
                                        game_state.buildings_group.add(new_building)
                                    elif recipe_data["result"] == "Anvil":
                                        new_building = Anvil(spawn_pos)
                                        game_state.buildings_group.add(new_building)
                                    elif recipe_data["result"] == "Monster Portal":
                                        new_building = MonsterPortal(spawn_pos)
                                        game_state.buildings_group.add(new_building)

                                    self.is_active = False
                                elif recipe_data["result"] in ["Pickaxe", "Axe"]:
                                    game_state.player_group.sprite.pitems.append(
                                        recipe_data["result"]
                                    )
                                    self.is_active = False
                                elif recipe_data["result"] in ["Monstahs"]:
                                    self.is_active = False
                                    game_state.effects_group.add(
                                        effects.Message(
                                            "Get Ready For Monsters",
                                            (255, 0, 0),
                                            game_state.zone,
                                        )
                                    )
                                    game_state.summon_timer = 180
                                else:
                                    game_state.add_to_inventory(recipe_data["result"])

                                # Break out to prevent dual-frame crafting clicks
                                break

                # Render text elements directly onto the card surface instead of the global screen
                text_surface = ui_font.render(r, True, (0, 0, 0))
                card_surf.blit(text_surface, (15, 15))

                ing_offset_y = 40
                for item_name, count in ingredients_dict.items():
                    ing_text = f"{item_name}: {count}"
                    ing_surface = ui_font.render(ing_text, True, (255, 255, 255))
                    card_surf.blit(ing_surface, (15, ing_offset_y))
                    ing_offset_y += 15

                # Perform the Pygame transformation scaling based on calculated scale factor
                current_scale = self.card_scales[r]
                scaled_w = int(130 * current_scale)
                scaled_h = int(130 * current_scale)

                if scaled_w > 0 and scaled_h > 0:
                    scaled_surf = pygame.transform.smoothscale(
                        card_surf, (scaled_w, scaled_h)
                    )
                    # Center the newly-scaled surface back perfectly over our default grid layout coordinates
                    center_x = current_x + 65
                    center_y = current_y + 65
                    scaled_rect = scaled_surf.get_rect(center=(center_x, center_y))
                    screen.blit(scaled_surf, scaled_rect)

                current_y += row_gap
                if current_y > 550:
                    current_y = start_y
                    current_x += row_gap


class Furnace(Building):
    def __init__(self, pos=None, layers=["base"]):
        super().__init__(pos)
        self.recipe_unlocked = True
        self.is_active = False
        self.click_cooldown = 0
        self.layers = layers
        self.crafting_rects = []

        # Dictionary to track the smooth scaling animation for each recipe card
        self.card_scales = {}

        # --- COAL SYSTEM VARIABLES ---
        self.coal_level = 0  # Remaining burn frames (0 means inactive)
        self.max_coal_level = 900  # 15 seconds at 60 FPS (15 * 60 = 900)
        self.button_scale = 1.0  # Smooth scaling value for "Add Coal" button

        pygame.draw.circle(self.image, (0, 0, 0), (30, 30), 15)
        pygame.draw.circle(self.image, (200, 200, 200), (30, 30), 15, 5)

    def update(self):
        super().update()
        if self.click_cooldown > 0:
            self.click_cooldown -= 1

        # Burn coal frame-by-frame if there is fuel remaining
        if self.coal_level > 0:
            self.coal_level -= 1

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.is_active = True

        if self.is_active and (
            pygame.key.get_pressed()[pygame.K_e]
            or pygame.key.get_pressed()[pygame.K_ESCAPE]
        ):
            self.is_active = False

    def draw_menu(self, screen):
        if not self.is_active:
            return

        inventory = game_state.inventory
        W, H = screen.get_size()

        # Draw main background panel
        pygame.draw.rect(screen, (100, 100, 100), (0, 0, W, H))
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, W, H), 10)

        # Main Title Shadow & Foreground
        title_surf = title_font.render("Furnacing", True, (50, 50, 155))
        title_rect = title_surf.get_rect(center=(W // 2 + 5, H - 95))
        screen.blit(title_surf, title_rect)

        title_surf = title_font.render("Furnacing", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(W // 2, H - 100))
        screen.blit(title_surf, title_rect)

        start_x = 150
        start_y = 150
        row_gap = 200
        current_y = start_y
        current_x = start_x

        # --- 1. RENDER CRAFTING CARDS ---
        for r in long_init_stuff.CRAFTING_RECIPES:
            recipe_data = long_init_stuff.CRAFTING_RECIPES[r]

            if recipe_data["building"] == "Furnace":
                ingredients_dict = recipe_data["ingredients"]
                card_rect = pygame.Rect(current_x, current_y, 150, 120)

                if r not in self.card_scales:
                    self.card_scales[r] = 1.0

                mouse_pos = pygame.mouse.get_pos()

                # Only allow hover effects if there is burning coal in the system
                is_hovered = card_rect.collidepoint(mouse_pos) and self.coal_level > 0
                target_scale = 1.5 if is_hovered else 1.0
                self.card_scales[r] += (target_scale - self.card_scales[r]) * 0.2

                # Create canvas space for card elements
                card_surf = pygame.Surface((160, 130), pygame.SRCALPHA)

                # Color theme: Gray/Blue normally, dull Dark Gray/Red if no fuel is burning
                header_color = (50, 50, 155) if self.coal_level > 0 else (40, 40, 50)
                body_color = (100, 100, 100) if self.coal_level > 0 else (70, 70, 75)
                outline_color = (10, 10, 10)

                pygame.draw.rect(
                    card_surf,
                    header_color,
                    pygame.Rect(10, 10, 150, 120),
                    border_radius=5,
                )
                pygame.draw.rect(
                    card_surf, body_color, (0, 30, 150, 90), border_radius=5
                )
                pygame.draw.rect(card_surf, outline_color, (0, 0, 150, 120), 10, 5)

                if is_hovered:
                    pygame.draw.rect(card_surf, (255, 127, 10), (0, 0, 150, 120), 10, 5)

                    if pygame.mouse.get_pressed()[0] and self.click_cooldown == 0:
                        self.click_cooldown = 15

                        current_counts = {}
                        for item in inventory:
                            if item != "empty":
                                current_counts[item] = current_counts.get(item, 0) + 1

                        can_craft = True
                        for ing_name, required_amount in ingredients_dict.items():
                            if current_counts.get(ing_name, 0) < required_amount:
                                can_craft = False
                                break

                        if can_craft:
                            for ing_name, required_amount in ingredients_dict.items():
                                removed = 0
                                for index in range(len(inventory)):
                                    if inventory[index] == ing_name:
                                        inventory[index] = "empty"
                                        removed += 1
                                        if removed == required_amount:
                                            break

                            game_state.add_to_inventory(recipe_data["result"])
                            break

                # Draw recipe title
                text_surface = ui_font.render(
                    r, True, (0, 0, 0) if self.coal_level > 0 else (100, 100, 100)
                )
                card_surf.blit(text_surface, (15, 15))

                # Draw ingredients list
                ing_offset_y = 40
                for item_name, count in ingredients_dict.items():
                    ing_text = f"{item_name}: {count}"
                    ing_surface = ui_font.render(
                        ing_text,
                        True,
                        (255, 255, 255) if self.coal_level > 0 else (150, 150, 150),
                    )
                    card_surf.blit(ing_surface, (15, ing_offset_y))
                    ing_offset_y += 15

                # Warn the player directly on the card if they need fuel
                if self.coal_level <= 0:
                    warn_surface = ui_font.render(
                        "Requires Fuel!", True, (255, 100, 100)
                    )
                    card_surf.blit(warn_surface, (15, 95))

                # Draw scaled canvas with smooth filters
                current_scale = self.card_scales[r]
                scaled_w = int(130 * current_scale)
                scaled_h = int(130 * current_scale)

                if scaled_w > 0 and scaled_h > 0:
                    scaled_surf = pygame.transform.smoothscale(
                        card_surf, (scaled_w, scaled_h)
                    )
                    center_x = current_x + 65
                    center_y = current_y + 65
                    scaled_rect = scaled_surf.get_rect(center=(center_x, center_y))
                    screen.blit(scaled_surf, scaled_rect)

                current_y += row_gap
                if current_y > 350:
                    current_y = start_y
                    current_x += row_gap

        # --- 2. RENDER THE INTERACTIVE COAL SLOT CONTROL PANEL (BOTTOM CENTER) ---
        btn_center_x = W // 2 - 110
        btn_center_y = H - 220
        btn_w, btn_h = 130, 36

        # Standard bounding box for mouse collision checks
        btn_rect = pygame.Rect(
            btn_center_x - btn_w // 2, btn_center_y - btn_h // 2, btn_w, btn_h
        )
        mouse_pos = pygame.mouse.get_pos()
        is_btn_hovered = btn_rect.collidepoint(mouse_pos)

        # Apply Bouncy Spring Animation math: (target - current) / 2
        target_btn_scale = 1.25 if is_btn_hovered else 1.0
        self.button_scale += (target_btn_scale - self.button_scale) / 2

        # Create localized button texture surface
        btn_surf = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
        btn_color = (220, 90, 40) if is_btn_hovered else (180, 70, 30)

        # Draw clean button edges
        pygame.draw.rect(btn_surf, btn_color, (0, 0, btn_w, btn_h), border_radius=6)
        pygame.draw.rect(
            btn_surf, (20, 20, 20), (0, 0, btn_w, btn_h), 3, border_radius=6
        )

        # Center button labels
        btn_text = ui_font.render("ADD COAL", True, (255, 255, 255))
        btn_text_rect = btn_text.get_rect(center=(btn_w // 2, btn_h // 2))
        btn_surf.blit(btn_text, btn_text_rect)

        # Draw scaled bouncy button to the main display
        scaled_btn_w = int(btn_w * self.button_scale)
        scaled_btn_h = int(btn_h * self.button_scale)
        if scaled_btn_w > 0 and scaled_btn_h > 0:
            scaled_btn_surf = pygame.transform.smoothscale(
                btn_surf, (scaled_btn_w, scaled_btn_h)
            )
            scaled_btn_rect = scaled_btn_surf.get_rect(
                center=(btn_center_x, btn_center_y)
            )
            screen.blit(scaled_btn_surf, scaled_rect := scaled_btn_rect)

        # Process adding coal when button is clicked
        if (
            is_btn_hovered
            and pygame.mouse.get_pressed()[0]
            and self.click_cooldown == 0
        ):
            self.click_cooldown = 20

            # Check inventory for Coal
            if "Coal" in inventory:
                # Remove exactly 1 Coal
                for index in range(len(inventory)):
                    if inventory[index] == "Coal":
                        inventory[index] = "empty"
                        break
                # Set active fuel levels
                self.coal_level = self.max_coal_level

                # Spawn a nice tiny cosmetic smoke/fire explosion
                game_state.effects_group.add(
                    effects.Pop(
                        self.pos.x,
                        self.pos.y,
                        15,
                        game_state.zone,
                        (255, 100, 0),
                    )
                )

        # --- 3. RENDER THE COAL BAR (TO THE RIGHT OF THE BUTTON) ---
        bar_x = W // 2 + 30
        bar_y = H - 235
        bar_w = 180
        bar_h = 30

        # Draw background tracker slot
        pygame.draw.rect(
            screen, (30, 30, 35), (bar_x, bar_y, bar_w, bar_h), border_radius=6
        )

        # Draw the active Orange Coal Level indicator
        if self.coal_level > 0:
            fill_width = int((bar_w - 6) * (self.coal_level / self.max_coal_level))
            if fill_width > 0:
                pygame.draw.rect(
                    screen,
                    (255, 110, 10),
                    (bar_x + 3, bar_y + 3, fill_width, bar_h - 6),
                    border_radius=4,
                )

        # Draw outer metal container borders
        pygame.draw.rect(
            screen, (200, 200, 200), (bar_x, bar_y, bar_w, bar_h), 2, border_radius=6
        )

        # Draw bar status text labels
        bar_status_str = (
            f"Fuel: {math.ceil(self.coal_level / 60)}s"
            if self.coal_level > 0
            else "NO COAL / OUT OF FUEL"
        )
        bar_text_color = (255, 255, 255) if self.coal_level > 0 else (240, 100, 100)
        bar_status_surf = ui_font.render(bar_status_str, True, bar_text_color)
        screen.blit(bar_status_surf, (bar_x + 8, bar_y + 8))


class Anvil(Building):
    def __init__(self, pos=None, layers=["base"]):
        super().__init__(pos)
        self.recipe_unlocked = True
        self.is_active = False
        self.click_cooldown = 0
        self.layers = layers
        self.crafting_rects = []

        # Dictionary to track the smooth scaling animation for each recipe card
        self.card_scales = {}

        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, (184, 115, 51), (0, 10, 80, 60), border_radius=5)
        pygame.draw.rect(self.image, (53, 87, 72), (0, 10, 80, 60), 10, 5)

        pygame.draw.line(self.image, ("grey"), (65, 50), (15, 30), 10)

    def update(self):
        super().update()
        if self.click_cooldown > 0:
            self.click_cooldown -= 1

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.is_active = True

        if (
            self.is_active
            and pygame.key.get_pressed()[pygame.K_e]
            or pygame.key.get_pressed()[pygame.K_ESCAPE]
        ):
            self.is_active = False

    def draw_menu(self, screen):
        if not self.is_active:
            return

        inventory = game_state.inventory
        W, H = screen.get_size()

        pygame.draw.rect(screen, (100, 100, 200), (0, 0, W, H))
        pygame.draw.rect(screen, (50, 50, 155), (0, 0, W, H), 10)

        pygame.draw.rect(screen, (100, 100, 100), (0, 0, W, H))
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, W, H), 10)

        title_surf = title_font.render("Anviling", True, (50, 50, 155))
        title_rect = title_surf.get_rect(center=(W // 2 + 5, H - 95))
        screen.blit(title_surf, title_rect)

        title_surf = title_font.render("Anviling", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(W // 2, H - 100))
        screen.blit(title_surf, title_rect)

        start_x = 150
        start_y = 150
        row_gap = 200
        current_y = start_y
        current_x = start_x

        for r in long_init_stuff.CRAFTING_RECIPES:
            recipe_data = long_init_stuff.CRAFTING_RECIPES[r]

            if recipe_data["building"] == "Anvil":
                ingredients_dict = recipe_data["ingredients"]

                # Updated to use the 150x120 card sizing
                card_rect = pygame.Rect(current_x, current_y, 150, 120)

                # Initialize scaling value for this specific card if not already tracked
                if r not in self.card_scales:
                    self.card_scales[r] = 1.0

                mouse_pos = pygame.mouse.get_pos()
                is_hovered = card_rect.collidepoint(mouse_pos)

                # Apply the Target Scale Math (Grow to 1.5 when hovered, sink back to 1.0 when not)
                target_scale = 1.5 if is_hovered else 1.0
                self.card_scales[r] += (target_scale - self.card_scales[r]) * 0.2

                # Create a temporary card surface to draw everything on (sized 160x130 to allow room for the shadow offset)
                card_surf = pygame.Surface((160, 130), pygame.SRCALPHA)

                pygame.draw.rect(
                    card_surf,
                    (50, 50, 155),
                    pygame.Rect(10, 10, 150, 120),
                    border_radius=5,
                )
                pygame.draw.rect(
                    card_surf,
                    (100, 100, 100),
                    (0, 30, 150, 90),
                    border_radius=5,
                )
                pygame.draw.rect(card_surf, (10, 10, 10), (0, 0, 150, 120), 10, 5)

                if is_hovered:
                    pygame.draw.rect(card_surf, (255, 127, 10), (0, 0, 150, 120), 10, 5)
                    if pygame.mouse.get_pressed()[0] and self.click_cooldown == 0:
                        self.click_cooldown = 15

                        current_counts = {}
                        for item in inventory:
                            if item != "empty":
                                current_counts[item] = current_counts.get(item, 0) + 1

                        can_craft = True
                        for ing_name, required_amount in ingredients_dict.items():
                            if current_counts.get(ing_name, 0) < required_amount:
                                can_craft = False
                                break

                        if can_craft:
                            for ing_name, required_amount in ingredients_dict.items():
                                removed = 0
                                for index in range(len(inventory)):
                                    if inventory[index] == ing_name:
                                        inventory[index] = "empty"
                                        removed += 1
                                        if removed == required_amount:
                                            break
                            if recipe_data["result"] in [
                                "Copper Pickaxe",
                                "Iron Pickaxe",
                            ]:
                                game_state.player_group.sprite.pitems.append(
                                    recipe_data["result"]
                                )
                            elif recipe_data["result"] in ["Super Ladder!"]:
                                game_state.buildings.add(
                                    SuperLadder(
                                        pygame.Vector2(
                                            random.randint(100, W // 2 - 100),
                                            random.randint(100, H // 2 - 100),
                                        )
                                    )
                                )
                            else:
                                game_state.add_to_inventory(recipe_data["result"])

                            # Break out to prevent dual-frame crafting clicks
                            break

                text_surface = ui_font.render(r, True, (0, 0, 0))
                card_surf.blit(text_surface, (15, 15))

                ing_offset_y = 40
                for item_name, count in ingredients_dict.items():
                    ing_text = f"{item_name}: {count}"
                    ing_surface = ui_font.render(ing_text, True, (255, 255, 255))
                    card_surf.blit(ing_surface, (15, ing_offset_y))
                    ing_offset_y += 15

                # Perform the Pygame transformation scaling based on calculated scale factor
                current_scale = self.card_scales[r]
                scaled_w = int(130 * current_scale)
                scaled_h = int(130 * current_scale)

                if scaled_w > 0 and scaled_h > 0:
                    scaled_surf = pygame.transform.smoothscale(
                        card_surf, (scaled_w, scaled_h)
                    )
                    # Center the newly-scaled surface back perfectly over our default grid layout coordinates
                    center_x = current_x + 65
                    center_y = current_y + 65
                    scaled_rect = scaled_surf.get_rect(center=(center_x, center_y))
                    screen.blit(scaled_surf, scaled_rect)

                current_y += row_gap
                if current_y > 550:
                    current_y = start_y
                    current_x += row_gap


class MineLadder(Building):
    def __init__(self, pos=None, layers=["base", "mine1"]):
        super().__init__(pos)
        pos = self.pos
        self.layers = layers
        self.entering = False

        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, (100, 100, 100), (40, 40), 30)
        pygame.draw.circle(self.image, (0, 0, 0), (40, 40), 25)
        pygame.draw.rect(
            self.image,
            (160, 82, 45),
            (25, 20, 30, 6),
            border_radius=1,
        )
        pygame.draw.rect(self.image, (0, 0, 0), (25, 20, 30, 6), 1, 1)
        pygame.draw.rect(self.image, (160, 82, 45), (15, 15, 15, 15), border_radius=1)
        pygame.draw.rect(self.image, (0, 0, 0), (15, 15, 15, 15), 1, 1)
        pygame.draw.rect(self.image, (160, 82, 45), (50, 15, 15, 15), border_radius=1)
        pygame.draw.rect(self.image, (0, 0, 0), (50, 15, 15, 15), 1, 1)

    def update(self):
        super().update()
        if game_state.zone in ["mine1", "base"]:
            if self.rect.collidepoint(game_state.player_group.sprite.pos):
                if not self.entering:
                    self.entering = True
                    if game_state.zone == "base":
                        game_state.zone = "mine1"
                        effects.add(
                            effects.Message("The Mine", (255, 255, 255), "mine1")
                        )
                    else:
                        game_state.zone = "base"
                        effects.add(
                            effects.Message("Your Base", (255, 255, 255), "base")
                        )
            else:
                self.entering = False


class SuperLadder(Building):
    def __init__(self, pos=None, layers=["base", "mine2"]):
        super().__init__(pos)
        pos = self.pos
        self.layers = layers
        self.entering = False

        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, (205, 155, 29), (40, 40), 30)
        pygame.draw.circle(self.image, (200, 50, 0), (40, 40), 25)
        pygame.draw.rect(
            self.image,
            (205, 155, 29),
            (25, 20, 30, 6),
            border_radius=1,
        )
        pygame.draw.rect(self.image, (0, 0, 0), (25, 20, 30, 6), 1, 1)
        pygame.draw.rect(self.image, (238, 201, 0), (15, 15, 15, 15), border_radius=1)
        pygame.draw.rect(self.image, (0, 0, 0), (15, 15, 15, 15), 1, 1)
        pygame.draw.rect(self.image, (238, 201, 0), (50, 15, 15, 15), border_radius=1)
        pygame.draw.rect(self.image, (0, 0, 0), (50, 15, 15, 15), 1, 1)

    def update(self):
        super().update()
        if game_state.zone in ["mine2", "base"]:
            if self.rect.collidepoint(game_state.player_group.sprite.pos):
                if not self.entering:
                    self.entering = True
                    if game_state.zone == "base":
                        game_state.zone = "mine2"
                        effects.add(
                            effects.Message("The Super Mine", (255, 200, 0), "mine2")
                        )
                    else:
                        game_state.zone = "base"
                        effects.add(
                            effects.Message("Your Base", (255, 255, 255), "base")
                        )
            else:
                self.entering = False


class MonsterPortal(Building):
    def __init__(self, pos=None, layers=["base", "The Outer Realm"]):
        super().__init__(pos)
        self.layers = layers
        self.entering = False
        self.timer = 0

        # Ensure the surface is large enough to fit the orbiting effect (160x160)
        self.image = pygame.Surface((160, 160), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)

        # Draw the base shapes once
        self.draw_portal_shapes()

    def draw_portal_shapes(self):
        """Draws the stationary portal base layers centered on the local image coordinates (80, 80)."""
        # 1. DRAW FIRST: The large outer alpha glow (Background layer)
        pygame.draw.circle(self.image, (255, 0, 255, 100), (80, 80), 40)

        # 2. DRAW SECOND: The main solid portal body (Middle layer)
        pygame.draw.circle(self.image, (255, 0, 255), (80, 80), 30)

        # 3. DRAW LAST: The sharp golden rim (Foreground layer)
        pygame.draw.circle(self.image, (125, 125, 0), (80, 80), 30, 7)

    def update(self):
        super().update()
        if game_state.zone in ["The Outer Realm", "base"]:
            if self.rect.collidepoint(game_state.player_group.sprite.pos):
                if not self.entering:
                    self.entering = True
                    if game_state.zone == "base":
                        game_state.zone = "The Outer Realm"
                        effects.add(
                            effects.Message(
                                "The Outer Realm", (255, 0, 255), "The Outer Realm"
                            )
                        )
                        game_state.screen_shake = 2
                    else:
                        game_state.zone = "base"
                        effects.add(
                            effects.Message("Your Base", (255, 255, 255), "base")
                        )
                        game_state.screen_shake = 2
            else:
                self.entering = False

        # Smoothly increment the orbit angle timer
        self.timer += 0.05
        if self.timer >= math.pi * 2:
            self.timer = 0

        # 1. Clear the surface so we don't leave trails of past positions
        self.image.fill((0, 0, 0, 0))

        # 2. Redraw the main portal body in the middle (80, 80)
        self.draw_portal_shapes()

        # 3. Draw the three orbiting magic energy orbs spaced evenly by 120 degrees (2pi/3 radians)
        orbit_radius = 60

        # Ball 1 (0 degrees offset)
        angle1 = self.timer
        orbit_x1 = 80 + int(orbit_radius * math.cos(angle1))
        orbit_y1 = 80 + int(orbit_radius * math.sin(angle1))
        pygame.draw.circle(self.image, (255, 100, 255), (orbit_x1, orbit_y1), 8)
        pygame.draw.circle(
            self.image,
            (255, 100, 255),
            (orbit_x1, orbit_y1),
            14 + 4 * math.sin(self.timer * 2),
            2,
        )

        # Ball 2 (120 degrees offset)
        angle2 = self.timer + (2 * math.pi / 3)
        orbit_x2 = 80 + int(orbit_radius * math.cos(angle2))
        orbit_y2 = 80 + int(orbit_radius * math.sin(angle2))
        pygame.draw.circle(self.image, (255, 100, 255), (orbit_x2, orbit_y2), 8)
        pygame.draw.circle(
            self.image,
            (255, 100, 255),
            (orbit_x2, orbit_y2),
            14 + 4 * math.sin(self.timer * 2),
            2,
        )

        # Ball 3 (240 degrees offset)
        angle3 = self.timer + (4 * math.pi / 3)
        orbit_x3 = 80 + int(orbit_radius * math.cos(angle3))
        orbit_y3 = 80 + int(orbit_radius * math.sin(angle3))
        pygame.draw.circle(self.image, (255, 100, 255), (orbit_x3, orbit_y3), 8)
        pygame.draw.circle(
            self.image,
            (255, 100, 255),
            (orbit_x3, orbit_y3),
            14 + 4 * math.sin(self.timer * 2),
            2,
        )
