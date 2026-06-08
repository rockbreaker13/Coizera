import abc
import math
import random
import pygame
from pygame import Vector2

from coizera import game_state
from coizera import effects


class BaseEnemy(pygame.sprite.Sprite, abc.ABC):
    """The abstract base class for all unique enemies.

    Forces all derived enemies to implement custom movement patterns and unique
    visual rendering.
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

        # Image surface preparation with PADDING to prevent edge clipping
        self.base_size = base_size

        # We add 30px padding around the surface canvas so squashing/stretching doesn't clip
        self.padding = 30
        self.surface_size = (
            base_size[0] + self.padding,
            base_size[1] + self.padding,
        )

        self._surface = pygame.Surface(self.surface_size, pygame.SRCALPHA).convert_alpha()
        self.image = self._surface.copy()
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        """Standard engine ticks that apply to every single enemy."""
        # 1. Track player direction and call the unique abstract behavior
        player_pos = game_state.player_group.sprite.pos
        direction = player_pos - self.pos

        # Call the customized abstract behavior (implemented by subclasses)
        self.update_behavior(direction)

        # Apply velocity and cap movement speeds
        self.pos += self.vel
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        # 2. Check for weapon slice hits & damage triggers
        weapon = game_state.weapon_group.sprite
        if self.rect.colliderect(weapon.rect):
            if weapon.is_swinging and not self.is_attacked:
                self.hp -= game_state.player_group.sprite.dmg
                self.is_attacked = True
                self.speed *= -0.5
                game_state.screen_shake = 1.5
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
        self.image.blit(self._surface, (0, 0))

    @abc.abstractmethod
    def update_behavior(self, direction_to_player):
        """All unique enemies must define how they move or attack the player."""
        pass

    def handle_death(self):
        """Triggers fancy explosion particle pops and distributes loot drop tiers."""
        # Particle explosion pop
        game_state.effects_group.add(
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
    """A classic, springy slime that squishes and stretches over time as it hops.

    Found in: 'base' and 'forest' zones.
    """

    def __init__(self, pos, zone):
        super().__init__(
            pos, zone, max_hp=10, max_speed=2.0, damage=1.5, base_size=(50, 40)
        )
        self.animation_timer = random.uniform(0, 10)
        self._draw_enemy()

    def update_behavior(self, direction_to_player):
        self.animation_timer += 0.15
        if direction_to_player.length() > 0:
            hop_boost = max(0.1, math.sin(self.animation_timer))
            self.vel = direction_to_player.normalize() * (self.speed * hop_boost)
        else:
            self.vel = Vector2(0, 0)
        
        self._draw_enemy()

    def _draw_enemy(self):
        self._surface.fill((0, 0, 0, 0))
        squash = 1.0 + (0.15 * math.sin(self.animation_timer))
        stretch = 1.0 - (0.15 * math.sin(self.animation_timer))

        width = int(self.base_size[0] * squash)
        height = int(self.base_size[1] * stretch)

        # Offset the coordinates to draw completely inside the center of our padded canvas
        offset_x = (self.surface_size[0] - width) // 2
        offset_y = self.surface_size[1] - height - (self.padding // 2)

        # Core green jelly bubble body
        body_rect = pygame.Rect(offset_x, offset_y, width, height)
        pygame.draw.ellipse(self._surface, (46, 204, 113), body_rect)
        pygame.draw.ellipse(self._surface, (39, 174, 96), body_rect, 4)  # Outline

        # Draw tiny cute facial eyes
        eye_y = body_rect.y + int(height * 0.4)
        left_eye_x = body_rect.x + int(width * 0.3)
        right_eye_x = body_rect.x + int(width * 0.7)
        pygame.draw.circle(self._surface, (0, 0, 0), (left_eye_x, eye_y), 3)
        pygame.draw.circle(self._surface, (0, 0, 0), (right_eye_x, eye_y), 3)


class ShadowStalker(BaseEnemy):
    """A terrifying creature that hides in shadows.

    It is almost completely invisible (transparent) when far away from the
    player, and slowly fades into focus as it stalks closer! Found in: 'The
    Outer Realm'.
    """

    def __init__(self, pos, zone):
        super().__init__(
            pos, zone, max_hp=20, max_speed=4, damage=4.0, base_size=(60, 60)
        )
        self.pulse = 0.0
        self.alpha = 20
        self._draw_enemy()

    def update_behavior(self, direction_to_player):
        self.pulse += 0.08
        dist = direction_to_player.length()

        if dist < 400:
            target_alpha = int(255 * (1.0 - (dist / 400.0)))
            self.alpha = max(25, target_alpha)
        else:
            self.alpha = 20

        if dist > 0:
            self.vel = direction_to_player.normalize() * self.speed
        else:
            self.vel = Vector2(0, 0)
            
        self._draw_enemy()

    def _draw_enemy(self):
        self._surface.fill((0, 0, 0, 0))
        # Match the expanded surface size to safely contain pulsing drawings
        shading_surf = pygame.Surface(self.surface_size, pygame.SRCALPHA)
        center_x = self.surface_size[0] // 2
        center_y = self.surface_size[1] // 2

        # Pulsing radius calculation tied to base size definitions
        radius = (self.base_size[0] // 2) - 5 + int(4 * math.sin(self.pulse))

        # Deep translucent purple core body
        pygame.draw.circle(
            shading_surf, (80, 0, 120, self.alpha), (center_x, center_y), radius
        )
        # Jagged sharp black crown outline
        pygame.draw.circle(
            shading_surf,
            (20, 0, 30, min(255, self.alpha)),
            (center_x, center_y),
            radius,
            4,
        )

        # Draw glowing red predator slashes for eyes
        eye_alpha = min(255, self.alpha * 2)
        eye_y = center_y - 5
        pygame.draw.line(
            shading_surf,
            (255, 0, 0, eye_alpha),
            (center_x - 12, eye_y - 4),
            (center_x - 3, eye_y + 4),
            3,
        )
        pygame.draw.line(
            shading_surf,
            (255, 0, 0, eye_alpha),
            (center_x + 12, eye_y - 4),
            (center_x + 3, eye_y + 4),
            3,
        )

        self._surface.blit(shading_surf, (0, 0))


class MagmaSlime(BaseEnemy):
    """A molten, fiery slime that leaves a trail of smoke and sparks behind as it

    slides. On death, it explodes and triggers a dynamic screen shake! Found in:
    'mine2' (the deep hot magma mines).
    """

    def __init__(self, pos, zone):
        super().__init__(
            pos, zone, max_hp=20, max_speed=2.5, damage=7.5, base_size=(50, 40)
        )
        self._draw_enemy()

    def update_behavior(self, direction_to_player):
        if direction_to_player.length() > 0:
            self.vel = direction_to_player.normalize() * self.speed
        else:
            self.vel = Vector2(0, 0)

        game_state.effects_group.add(
            effects.Twinkle(
                self.pos.copy()
                + Vector2(random.randint(-20, 20), random.randint(-20, 20)),
                random.randint(4, 8),
                self.zone,
                (255, random.randint(0, 255), 0),
            )
        )
        
        self._draw_enemy()

    def _draw_enemy(self):
        self._surface.fill((0, 0, 0, 0))
        center_x = self.surface_size[0] // 2
        center_y = self.surface_size[1] // 2

        # Draw relative to center alignment points instead of hard (0,0) bounds
        offset_x = (self.surface_size[0] - self.base_size[0]) // 2
        offset_y = (self.surface_size[1] - self.base_size[1]) // 2

        # Outer boiling magma shield
        pygame.draw.ellipse(
            self._surface,
            (255, 60, 0),
            (offset_x, offset_y, self.base_size[0], self.base_size[1]),
        )

        # Bright yellow-hot liquid core
        pygame.draw.ellipse(
            self._surface,
            (255, 200, 0),
            (
                offset_x + 6,
                offset_y + 6,
                self.base_size[0] - 12,
                self.base_size[1] - 12,
            ),
        )

        # Sharp black rock fragments floating safely inside
        pygame.draw.circle(self._surface, (30, 20, 20), (center_x - 12, center_y - 8), 5)
        pygame.draw.circle(self._surface, (30, 20, 20), (center_x + 12, center_y - 4), 6)
        pygame.draw.circle(self._surface, (30, 20, 20), (center_x, center_y + 10), 4)
