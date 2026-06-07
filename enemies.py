import pygame
from pygame import Vector2
import random
import math
import abc
import sys


# Dynamic reference helper to safely access groups and variables from the main script
def get_main():
    return sys.modules["__main__"]


class BaseEnemy(pygame.sprite.Sprite, abc.ABC):
    """
    The abstract base class for all unique enemies.
    Forces all derived enemies to implement custom movement patterns and unique visual rendering.
    """

    def __init__(self, pos, zone, max_hp, max_speed, damage, base_size=(60, 60)):
        super().__init__()
        self.pos = Vector2(pos)
        self.zone = zone

        # Health & State stats
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_speed = max_speed
        self.speed = 0.0
        self.dmg = damage

        # State tracking flags
        self.is_attacked = False
        self.vel = Vector2(0, 0)

        # Image surface preparation
        self.base_size = base_size
        self.image = pygame.Surface(base_size, pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        """Standard engine ticks that apply to every single enemy."""
        main_mod = get_main()

        # 1. Track player direction and call the unique abstract behavior
        player_pos = main_mod.player.sprite.pos
        direction = player_pos - self.pos

        # Call the customized abstract behavior (implemented by subclasses)
        self.update_behavior(direction)

        # Apply velocity and cap movement speeds
        self.pos += self.vel
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        # 2. Check for weapon slice hits & damage triggers
        weapon = main_mod.weapon.sprite
        if rect_hits := self.rect.colliderect(weapon.rect):
            if weapon.is_swinging and not self.is_attacked:
                self.hp -= main_mod.player.sprite.dmg
                self.is_attacked = True
                self.speed *= 0.2
        else:
            self.is_attacked = False

        # Apply friction to drag speed values smoothly
        if self.speed < self.max_speed:
            self.speed += 0.2
        else:
            self.speed *= 0.85

        # 3. Handle death and drop reward assets
        if self.hp <= 0:
            self.handle_death()
            self.kill()
            return

        # 4. Draw customized unique animations on the fly
        self.image.fill((0, 0, 0, 0))  # Clean surface background
        self.draw_visuals()

    @abc.abstractmethod
    def update_behavior(self, direction_to_player):
        """All unique enemies must define how they move or attack the player."""
        pass

    @abc.abstractmethod
    def draw_visuals(self):
        """All unique enemies must draw their own distinct shapes and faces onto self.image."""
        pass

    def handle_death(self):
        """Triggers fancy explosion particle pops and distributes loot drop tiers."""
        main_mod = get_main()
        import items
        import effects

        # Particle explosion pop
        main_mod.effects_group.add(
            effects.Pop(
                self.pos.x,
                self.pos.y,
                self.base_size[0] + 10,
                self.zone,
                self.get_particle_color(),
            )
        )

        # Spawn random loot drops based on our enemy class definitions
        self.drop_loot()

    def get_particle_color(self):
        """Override this in your custom class for customized explosion colors!"""
        return (100, 100, 100)

    def drop_loot(self):
        """Override this in your custom class to specify unique loot items."""
        pass


# =====================================================================
# --- CONCRETE UNIQUE ENEMIES ---
# =====================================================================


class BouncingSlime(BaseEnemy):
    """
    A classic, springy slime that squishes and stretches over time as it hops.
    Found in: 'base' and 'forest' zones.
    """

    def __init__(self, pos, zone):
        super().__init__(
            pos, zone, max_hp=10, max_speed=2.0, damage=1.5, base_size=(60, 50)
        )
        self.animation_timer = random.uniform(0, 10)

    def update_behavior(self, direction_to_player):
        # Move directly towards player with a slight slithering/hopping speed boost
        self.animation_timer += 0.15

        if direction_to_player.length() > 0:
            # We move faster on the peak of our bouncy sine wave, mimicking real hops!
            hop_boost = max(0.1, math.sin(self.animation_timer))
            self.vel = direction_to_player.normalize() * (self.speed * hop_boost)
        else:
            self.vel = Vector2(0, 0)

    def draw_visuals(self):
        # Create a squash and stretch bouncy scale value
        squash = 1.0 + (0.15 * math.sin(self.animation_timer))
        stretch = 1.0 - (0.15 * math.sin(self.animation_timer))

        width = int(self.base_size[0] * squash)
        height = int(self.base_size[1] * stretch)

        # Core green jelly bubble body
        body_rect = pygame.Rect(
            (self.base_size[0] - width) // 2,
            (self.base_size[1] - height),
            width,
            height,
        )
        pygame.draw.ellipse(self.image, (46, 204, 113), body_rect)
        pygame.draw.ellipse(self.image, (39, 174, 96), body_rect, 4)  # Outline

        # Draw tiny cute facial eyes
        eye_y = body_rect.y + int(height * 0.4)
        left_eye_x = body_rect.x + int(width * 0.3)
        right_eye_x = body_rect.x + int(width * 0.7)
        pygame.draw.circle(self.image, (0, 0, 0), (left_eye_x, eye_y), 3)
        pygame.draw.circle(self.image, (0, 0, 0), (right_eye_x, eye_y), 3)

    def get_particle_color(self):
        return (46, 204, 113)

    def drop_loot(self):
        main_mod = get_main()
        import items

        if random.randint(1, 3) == 1:
            self.loot_table = [items.Grass, items.Copper]
            main_mod.items_group.add(
                random.choice(self.loot_table)(
                    self.pos.copy()
                    + Vector2(random.randint(-20, 20), random.randint(-20, 20)),
                    self.zone,
                )
            )


class ShadowStalker(BaseEnemy):
    """
    A terrifying creature that hides in shadows. It is almost completely invisible (transparent)
    when far away from the player, and slowly fades into focus as it stalks closer!
    Found in: 'The Outer Realm'.
    """

    def __init__(self, pos, zone):
        super().__init__(
            pos, zone, max_hp=20, max_speed=7, damage=4.0, base_size=(70, 70)
        )
        self.pulse = 0.0
        self.alpha = 20

    def update_behavior(self, direction_to_player):
        self.pulse += 0.08
        dist = direction_to_player.length()

        # Calculate dynamic alpha based on closeness: invisible far away, visible up close!
        if dist < 400:
            target_alpha = int(255 * (1.0 - (dist / 400.0)))
            self.alpha = max(25, target_alpha)
        else:
            self.alpha = 20

        if dist > 0:
            self.vel = direction_to_player.normalize() * self.speed
        else:
            self.vel = Vector2(0, 0)

    def draw_visuals(self):
        # Build transparent shadow-cloak surface
        shading_surf = pygame.Surface(self.base_size, pygame.SRCALPHA)
        center = self.base_size[0] // 2

        # Pulsing radius
        radius = center - 5 + int(4 * math.sin(self.pulse))

        # Deep translucent purple core body
        pygame.draw.circle(
            shading_surf, (80, 0, 120, self.alpha), (center, center), radius
        )
        # Jagged sharp black crown outline
        pygame.draw.circle(
            shading_surf,
            (20, 0, 30, min(255, self.alpha)),
            (center, center),
            radius,
            4,
        )

        # Draw glowing red predator slashes for eyes
        eye_alpha = min(255, self.alpha * 2)
        eye_y = center - 5
        pygame.draw.line(
            shading_surf,
            (255, 0, 0, eye_alpha),
            (center - 12, eye_y - 4),
            (center - 3, eye_y + 4),
            3,
        )
        pygame.draw.line(
            shading_surf,
            (255, 0, 0, eye_alpha),
            (center + 12, eye_y - 4),
            (center + 3, eye_y + 4),
            3,
        )

        self.image.blit(shading_surf, (0, 0))

    def get_particle_color(self):
        return (80, 0, 120)

    def drop_loot(self):
        main_mod = get_main()
        import items

        if random.randint(1, 2) == 1:
            self.loot_table = [items.IronIngot, items.IronRod, items.AncientParts]
            main_mod.items_group.add(
                random.choice(self.loot_table)(
                    self.pos.copy()
                    + Vector2(random.randint(-20, 20), random.randint(-20, 20)),
                    self.zone,
                )
            )


class MagmaSlime(BaseEnemy):
    """
    A molten, fiery slime that leaves a trail of smoke and sparks behind as it slides.
    On death, it explodes and triggers a dynamic screen shake!
    Found in: 'mine2' (the deep hot magma mines).
    """

    def __init__(self, pos, zone):
        super().__init__(
            pos, zone, max_hp=20, max_speed=2.5, damage=7.5, base_size=(60, 50)
        )

    def update_behavior(self, direction_to_player):
        main_mod = get_main()
        import effects

        # Slither slowly
        if direction_to_player.length() > 0:
            self.vel = direction_to_player.normalize() * self.speed
        else:
            self.vel = Vector2(0, 0)

        # Periodically leave sparkling orange ember effects on the floor!
        main_mod.effects_group.add(
            effects.Twinkle(
                self.pos.copy()
                + Vector2(random.randint(-20, 20), random.randint(-20, 20)),
                4,
                self.zone,
                (255, random.randint(0, 255), 0),
            )
        )

    def draw_visuals(self):
        center_x = self.base_size[0] // 2
        center_y = self.base_size[1] // 2

        # Outer boiling magma shield
        pygame.draw.ellipse(
            self.image, (255, 60, 0), (0, 0, self.base_size[0], self.base_size[1])
        )

        # Bright yellow-hot liquid core
        pygame.draw.ellipse(
            self.image,
            (255, 200, 0),
            (6, 6, self.base_size[0] - 12, self.base_size[1] - 12),
        )

        # Sharp black rock fragments floating on top
        pygame.draw.circle(self.image, (30, 20, 20), (center_x - 12, center_y - 8), 5)
        pygame.draw.circle(self.image, (30, 20, 20), (center_x + 12, center_y - 4), 6)
        pygame.draw.circle(self.image, (30, 20, 20), (center_x, center_y + 10), 4)

    def get_particle_color(self):
        return (255, 60, 0)

    def drop_loot(self):
        main_mod = get_main()
        import items

        # Drops raw glowing magmatite!
        if random.randint(1, 3) == 1:
            self.loot_table = [items.Magmatite, items.Iron]
            main_mod.items_group.add(
                random.choice(self.loot_table)(
                    self.pos.copy()
                    + Vector2(random.randint(-20, 20), random.randint(-20, 20)),
                    self.zone,
                )
            )
