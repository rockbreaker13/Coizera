import pygame
from abc import ABC, abstractmethod
import random
import math
import sys

main_mod = sys.modules["__main__"]


# Base abstract structural class representing ground collectables
class Item(pygame.sprite.Sprite, ABC):

    def __init__(self, pos, zone):
        super().__init__()
        # self.pos acts as your permanent, unaltered logical coordinate
        self.pos = pygame.math.Vector2(pos)
        self.offset_pos = pos
        self.zone = zone
        self.shadow = pygame.Surface((240, 240), pygame.SRCALPHA).convert_alpha()

        self.animation_time = 0.0
        self.animation_duration = 0.6
        self.is_spawning = True
        self.scale = 0.0
        self.original_image = None
        self.target_scale = 1
        self.timer = random.randint(600, 2400)

        # Start offset high so it "drops" down to 0
        self.y_offset = 30

        # Collection animation states
        self.is_collecting = False
        self.collection_progress = 0.0

    @abstractmethod
    def apply(self):
        pass

    def collect(self):
        """Triggers the smooth absorption collection animation."""
        if not self.is_collecting:
            self.is_collecting = True
            self.is_spawning = False  # Stop regular drop/spawn calculations

    def update(self):
        if self.original_image is None:
            self.original_image = self.image.copy()

        # 1. Normal Spawning Drop Animation
        if self.is_spawning:
            self.scale += (self.target_scale - self.scale) * 0.2

            # y_offset naturally approaches 0 over time
            self.y_offset += (0 - self.y_offset) * 0.2

            new_width = int(self.original_image.get_width() * self.scale)
            new_height = int(self.original_image.get_height() * self.scale)

            if new_width > 0 and new_height > 0:
                self.image = pygame.transform.scale(
                    self.original_image, (new_width, new_height)
                )
            else:
                self.image = pygame.Surface((0, 0), pygame.SRCALPHA)

            # Stop spawning calculations when close to target
            if abs(self.scale - self.target_scale) < 0.01 and abs(self.y_offset) < 0.1:
                self.scale = self.target_scale
                self.y_offset = 0
                self.is_spawning = False

        # 2. Smooth Vacuum Collection Animation (Lerp toward Player & Scale Down)
        elif self.is_collecting:
            # Gradually increase collection progress towards 1.0 (completion)
            self.collection_progress += (1.0 - self.collection_progress) * 0.2

            # Safely fetch the player's current position from the main module
            if hasattr(main_mod, "player") and main_mod.player.sprite:
                player_pos = main_mod.player.sprite.pos

                # Smoothly slide (lerp) the item's world position directly into the player!
                # Formula: current + (target - current) * progress
                self.pos.x += (player_pos.x - self.pos.x) * 0.25
                self.pos.y += (player_pos.y - self.pos.y) * 0.25

            # Smoothly shrink the item scale to zero as it approaches the player
            self.scale = max(0.0, 1.0 - self.collection_progress)

            new_width = int(self.original_image.get_width() * self.scale)
            new_height = int(self.original_image.get_height() * self.scale)

            if new_width > 0 and new_height > 0:
                self.image = pygame.transform.scale(
                    self.original_image, (new_width, new_height)
                )
            else:
                self.image = pygame.Surface((0, 0), pygame.SRCALPHA)

            # Once the collection animation is fully complete (shrunk to near zero), kill the sprite
            if self.collection_progress >= 0.95:
                self.kill()

        # Regular item aging / despawning (only if not being collected)
        if not self.is_collecting:
            self.timer -= 1
            if self.timer < 0:
                current_alpha = max(0, 255 + self.timer)
                self.image.set_alpha(current_alpha)
                if current_alpha <= 0:
                    self.kill()

        # Calculate visual coordinate and update the rect boundary
        render_y = self.pos.y + self.y_offset
        self.rect = self.image.get_rect(center=(self.pos.x, render_y))


class Stick(Item):
    def __init__(self, pos, zone):
        super().__init__(pos, zone)
        # Surface height increased to 40 to fit shadow under the stick
        self.image = pygame.Surface((60, 40), pygame.SRCALPHA)
        # Flat ground shadow drawn at the bottom
        pygame.draw.ellipse(self.image, (0, 0, 0, 100), (0, 20, 60, 15))
        # Stick model drawn above the shadow
        pygame.draw.rect(self.image, (139, 69, 19), (0, 10, 60, 20), border_radius=3)
        pygame.draw.rect(self.image, (0, 0, 0), (0, 10, 60, 20), 5, 3)
        self.rect = self.image.get_rect(center=self.pos)
        self.name = "Stick"

    def apply(self):
        pass


class Rock(Item):
    def __init__(self, pos, zone):
        super().__init__(pos, zone)
        # Surface height increased to 80 to fit shadow under the rock
        self.image = pygame.Surface((60, 80), pygame.SRCALPHA)
        # Flat ground shadow drawn at the bottom
        pygame.draw.ellipse(self.image, (0, 0, 0, 100), (0, 60, 60, 15))
        # Rock model drawn above the shadow
        pygame.draw.rect(self.image, (127, 127, 127), (0, 5, 60, 60), border_radius=10)
        pygame.draw.rect(self.image, (0, 0, 0), (0, 5, 60, 60), 5, 10)
        self.rect = self.image.get_rect(center=self.pos)
        self.name = "Rock"

    def apply(self):
        pass


class Grass(Item):
    def __init__(self, pos, zone):
        super().__init__(pos, zone)
        # Surface height increased to 80 to fit shadow under the grass
        self.image = pygame.Surface((60, 80), pygame.SRCALPHA)
        # Flat ground shadow drawn at the bottom
        pygame.draw.ellipse(self.image, (0, 0, 0, 100), (0, 60, 60, 15))
        # Grass model drawn above the shadow (offset by y=5)
        pygame.draw.polygon(
            self.image,
            (0, 127, 0),
            [(0, 5), (10, 65), (50, 65), (60, 5), (40, 35), (30, 5), (20, 35)],
        )
        pygame.draw.polygon(
            self.image,
            (0, 50, 0),
            [(0, 5), (10, 65), (50, 65), (60, 5), (40, 35), (30, 5), (20, 35)],
            5,
        )
        self.rect = self.image.get_rect(center=self.pos)
        self.name = "Grass"

    def apply(self):
        pass


class Iron(Item):
    def __init__(self, pos, zone):
        super().__init__(pos, zone)
        # Surface height increased to 80 to fit shadow under the iron ore
        self.image = pygame.Surface((60, 80), pygame.SRCALPHA)
        # Flat ground shadow drawn at the bottom
        pygame.draw.ellipse(self.image, (0, 0, 0, 100), (0, 60, 60, 15))
        # Iron ore model drawn above the shadow
        pygame.draw.rect(self.image, (127, 127, 127), (0, 5, 60, 60), border_radius=10)
        pygame.draw.rect(self.image, (0, 0, 0), (0, 5, 60, 60), 5, 10)

        # Draw ore details (re-offset by y=5 to stay inside model)
        poly1_points = [(15, 17), (28, 15), (32, 27), (18, 31)]
        poly2_points = [(35, 37), (48, 30), (52, 45), (38, 53)]
        poly3_points = [(12, 43), (22, 40), (25, 53), (14, 51)]

        pygame.draw.polygon(self.image, (165, 42, 42), poly1_points)
        pygame.draw.polygon(self.image, (178, 34, 34), poly2_points)
        pygame.draw.polygon(self.image, (139, 0, 0), poly3_points)

        pygame.draw.polygon(self.image, (0, 0, 0), poly1_points, 1)
        pygame.draw.polygon(self.image, (0, 0, 0), poly2_points, 1)
        pygame.draw.polygon(self.image, (0, 0, 0), poly3_points, 1)

        self.rect = self.image.get_rect(center=self.pos)
        self.name = "Iron"
        self.tool = "Copper Pickaxe"

    def apply(self):
        pass


class Copper(Item):
    def __init__(self, pos, zone):
        super().__init__(pos, zone)
        # Surface height increased to 80 to fit shadow under the iron ore
        self.image = pygame.Surface((60, 80), pygame.SRCALPHA)
        # Flat ground shadow drawn at the bottom
        pygame.draw.ellipse(self.image, (0, 0, 0, 100), (0, 60, 60, 15))
        # Iron ore model drawn above the shadow
        pygame.draw.rect(self.image, (127, 127, 127), (0, 5, 60, 60), border_radius=10)
        pygame.draw.rect(self.image, (0, 0, 0), (0, 5, 60, 60), 5, 10)

        # Draw ore details (re-offset by y=5 to stay inside model)
        poly1_points = [(15, 17), (28, 15), (32, 27), (18, 31)]
        poly2_points = [(35, 37), (48, 30), (52, 45), (38, 53)]
        poly3_points = [(12, 43), (22, 40), (25, 53), (14, 51)]

        pygame.draw.polygon(self.image, (184, 115, 51), poly1_points)
        pygame.draw.polygon(self.image, (78, 117, 102), poly2_points)
        pygame.draw.polygon(self.image, (112, 181, 150), poly3_points)

        pygame.draw.polygon(self.image, (0, 0, 0), poly1_points, 1)
        pygame.draw.polygon(self.image, (0, 0, 0), poly2_points, 1)
        pygame.draw.polygon(self.image, (0, 0, 0), poly3_points, 1)

        self.rect = self.image.get_rect(center=self.pos)
        self.name = "Copper"
        self.tool = "Pickaxe"

    def apply(self):
        pass


class Coal(Item):
    def __init__(self, pos, zone):
        super().__init__(pos, zone)
        # Surface height increased to 80 to fit shadow under the coal
        self.image = pygame.Surface((60, 80), pygame.SRCALPHA)
        # Flat ground shadow drawn at the bottom
        pygame.draw.ellipse(self.image, (0, 0, 0, 100), (0, 60, 60, 15))
        # Coal model drawn above the shadow
        pygame.draw.rect(self.image, (20, 20, 20), (0, 5, 60, 60), border_radius=10)
        pygame.draw.rect(self.image, (50, 50, 50), (0, 5, 60, 60), 5, 10)
        self.rect = self.image.get_rect(center=self.pos)
        self.name = "Coal"

    def apply(self):
        pass


class Tree(Item):
    def __init__(self, pos, zone):
        super().__init__(pos, zone)
        # Tree surface is already 240x240, which leaves plenty of space for the shadow!
        self.image = pygame.Surface((240, 240), pygame.SRCALPHA)
        # Shadow drawn underneath the trunk
        pygame.draw.ellipse(self.image, (0, 0, 0, 100), (40, 180, 160, 50))
        # Trunk and roots drawn on top of the shadow
        pygame.draw.rect(self.image, (74, 30, 24), (85, 95, 70, 110))
        pygame.draw.circle(self.image, (74, 30, 24), (120, 200), (35))
        pygame.draw.rect(self.image, ("brown"), (90, 100, 60, 100))
        pygame.draw.circle(self.image, ("brown"), (120, 200), (30))
        # Leaves drawn on top
        pygame.draw.circle(self.image, (0, 150, 0), (120, 100), 90)
        pygame.draw.circle(self.image, ("green"), (120, 100), 80)
        self.rect = self.image.get_rect(center=self.pos)
        self.name = "Tree Log"
        self.tool = "Axe"

    def apply(self):
        pass


class AncientParts(Item):
    def __init__(self, pos, zone):
        super().__init__(pos, zone)
        self.image = pygame.Surface((240, 240), pygame.SRCALPHA)

        # 1. Ground Shadow (flat black transparency)
        pygame.draw.ellipse(self.image, (0, 0, 0, 100), (40, 175, 160, 50))

        # Color Palette for Brass
        brass_dark = (139, 105, 20)
        brass_med = (205, 155, 29)
        brass_light = (238, 201, 0)
        black = (0, 0, 0)

        # 2. Draw a hexagonal 3D Brass Bolt
        # Head Vertices (Center of head is at 90, 110)
        top_face = [(90, 110), (65, 100), (90, 90), (115, 100)]
        left_face = [(90, 110), (65, 100), (65, 120), (90, 130)]
        right_face = [(90, 110), (115, 100), (115, 120), (90, 130)]

        # Fill 3D Hex facets with different brightness values to create lighting depth
        pygame.draw.polygon(self.image, brass_light, top_face)
        pygame.draw.polygon(self.image, brass_dark, left_face)
        pygame.draw.polygon(self.image, brass_med, right_face)

        # Draw black outlines around the hexagon faces to keep your clean style
        pygame.draw.polygon(self.image, black, top_face, 4)
        pygame.draw.polygon(self.image, black, left_face, 4)
        pygame.draw.polygon(self.image, black, right_face, 4)

        # Bolt Shaft (extending rightwards)
        pygame.draw.rect(self.image, brass_med, (115, 108, 65, 24))
        pygame.draw.rect(self.image, black, (115, 108, 65, 24), 4)

        # Bolt Threads (Ridges)
        for tx in [125, 134, 143, 152, 161, 170]:
            pygame.draw.line(self.image, brass_dark, (tx, 110), (tx, 130), 4)
            pygame.draw.line(self.image, brass_light, (tx - 2, 110), (tx - 2, 122), 2)

        # 3. Draw a Brass Screw crossed next to the bolt
        # Head (Centered around 140, 150)
        pygame.draw.ellipse(self.image, brass_med, (120, 135, 40, 30))
        pygame.draw.ellipse(self.image, black, (120, 135, 40, 30), 4)

        # Screw Slot (flathead)
        pygame.draw.line(self.image, black, (126, 153), (154, 147), 5)

        # 4. Draw a flat Brass Washer lying at the bottom
        pygame.draw.ellipse(self.image, brass_med, (70, 145, 45, 25))
        pygame.draw.ellipse(self.image, black, (70, 145, 45, 25), 4)
        # Inside cutout hole of the washer
        pygame.draw.ellipse(self.image, (40, 100, 20), (83, 152, 18, 11))
        pygame.draw.ellipse(self.image, black, (83, 152, 18, 11), 3)

        self.rect = self.image.get_rect(center=self.pos)
        self.name = "Old Parts"

    def apply(self):
        pass


class DarkEssence(Item):
    def __init__(self, pos, zone):
        super().__init__(pos, zone)
        self.image = pygame.Surface((240, 240), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (0, 0, 0, 100), (40, 180, 160, 50))

        pygame.draw.circle(self.image, (0, 0, 0), (120, 120), 60)
        pygame.draw.circle(self.image, (100, 0, 175), (120, 120), 60, 10)
        self.rect = self.image.get_rect(center=self.pos)
        self.name = "Darkness"

    def apply(self):
        pass


class IronIngot(Item):
    def __init__(self, pos, zone):
        super().__init__(pos, zone)
        # Surface height increased to 80 to fit shadow under the iron ore
        self.image = pygame.Surface((60, 80), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (0, 0, 0, 100), (0, 45, 60, 15))

        # Ingot body shifted up by 5 pixels to sit right on top of the shadow
        pygame.draw.polygon(
            self.image,
            (210, 100, 50),
            [(25, 35), (10, 35), (10, 20), (25, 5), (40, 5), (40, 20)],
        )
        pygame.draw.rect(self.image, (100, 50, 50), (10, 20, 16, 16), 3)
        pygame.draw.lines(
            self.image,
            (100, 50, 50),
            False,
            [(10, 20), (25, 5), (40, 5), (40, 20), (25, 35)],
            3,
        )
        pygame.draw.line(self.image, (100, 50, 50), (25, 20), (40, 5), 3)

        self.rect = self.image.get_rect(center=self.pos)
        self.name = "Iron Ingot"

    def apply(self):
        pass


class IronRod(Item):
    def __init__(self, pos, zone):
        super().__init__(pos, zone)
        # Surface height increased to 80 to fit shadow under the iron ore
        self.image = pygame.Surface((60, 80), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (0, 0, 0, 100), (0, 45, 60, 15))

        pygame.draw.polygon(
            self.image,
            (100, 50, 50),
            [
                (43, 3),  # Top-right side offset
                (57, 17),  # Alternative top-right corner
                (17, 57),  # Bottom-left side offset
                (3, 43),  # Alternative bottom-left corner
            ],
        )

        # 2. Main joints (Drawn over the polygon connectors so they blend seamlessly)
        pygame.draw.circle(self.image, (100, 50, 50), (50, 10), 10)
        pygame.draw.circle(self.image, (210, 100, 50), (10, 50), 10)
        pygame.draw.circle(self.image, (100, 50, 50), (10, 50), 10, 3)
        self.rect = self.image.get_rect(center=self.pos)
        self.name = "Iron Rod"

    def apply(self):
        pass


class Magmatite(Item):
    def __init__(self, pos, zone):
        super().__init__(pos, zone)
        # Surface height increased to 80 to fit shadow under the ore
        self.image = pygame.Surface((60, 80), pygame.SRCALPHA)

        # Flat ground shadow drawn at the bottom
        pygame.draw.ellipse(self.image, (0, 0, 0, 100), (0, 60, 60, 15))

        # Imperfect circle base for the volcanic rock (dark grey/charcoal)
        pygame.draw.ellipse(self.image, (120, 90, 60), (2, 5, 56, 56))  # Main body
        pygame.draw.ellipse(
            self.image, (100, 45, 48), (5, 8, 48, 48)
        )  # Inner texture variation
        pygame.draw.ellipse(self.image, (0, 0, 0), (2, 5, 56, 56), 4)  # Outline

        # Lava color palette
        orange = (255, 140, 0)
        red_orange = (255, 69, 0)
        red = (255, 0, 0)

        # Pick 1 of 3 hand-crafted, beautiful root patterns so it varies slightly
        pattern_choice = random.randint(1, 3)

        if pattern_choice == 1:
            # Pattern 1: Central lightning crack branching left and right
            pygame.draw.line(
                self.image, orange, (30, 20), (25, 35), width=5
            )  # Main trunk
            pygame.draw.line(self.image, orange, (25, 35), (35, 48), width=4)
            pygame.draw.line(
                self.image, red_orange, (25, 35), (15, 42), width=3
            )  # Left branch
            pygame.draw.line(self.image, red, (15, 42), (18, 52), width=2)
            pygame.draw.line(
                self.image, red_orange, (35, 48), (40, 40), width=3
            )  # Right branch

        elif pattern_choice == 2:
            # Pattern 2: Heavy right side root flowing downward
            pygame.draw.line(
                self.image, red_orange, (40, 22), (38, 36), width=5
            )  # Main trunk
            pygame.draw.line(self.image, orange, (38, 36), (44, 46), width=4)
            pygame.draw.line(
                self.image, red_orange, (38, 36), (26, 42), width=3
            )  # Sweeping left branch
            pygame.draw.line(self.image, red, (26, 42), (20, 35), width=2)
            pygame.draw.line(self.image, red, (26, 42), (28, 52), width=2)

        else:
            # Pattern 3: Wide split root system anchoring the center
            pygame.draw.line(
                self.image, orange, (28, 25), (32, 38), width=5
            )  # Center node
            pygame.draw.line(
                self.image, red_orange, (28, 25), (16, 22), width=3
            )  # High left crack
            pygame.draw.line(
                self.image, orange, (32, 38), (22, 48), width=4
            )  # Low left branch
            pygame.draw.line(
                self.image, red_orange, (32, 38), (42, 44), width=4
            )  # Low right branch
            pygame.draw.line(self.image, red, (42, 44), (40, 40), width=2)

        self.rect = self.image.get_rect(center=self.pos)
        self.name = "Magmatite"
        self.tool = "Iron Pickaxe"

    def apply(self):
        pass
