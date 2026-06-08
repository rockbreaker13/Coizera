import pygame
import math

from coizera import game_state
from coizera import effects


class Projectile(pygame.sprite.Sprite):
    def __init__(self, is_from, kind, pos, speed, direction, zone):
        super().__init__()
        self.is_from = is_from
        self.kind = kind
        self.zone = zone

        # Store positions as floating-point vectors for smooth movement
        self.pos = pygame.math.Vector2(pos)
        self.speed = speed

        # 1. Normalize the direction vector so its total length equals 1
        if direction.length() > 0:
            self.direction = direction.normalize()
        else:
            self.direction = pygame.math.Vector2(1, 0)  # Default to East if zero length

        if self.kind.strip().lower() == "fire":
            self.image = pygame.Surface((100, 100), pygame.SRCALPHA).convert_alpha()

            # Draw from largest (outermost/most transparent) to smallest (innermost/opaque)
            for i in reversed(range(10)):
                # Smooth transparency curve: scale linearly so outer rings are very faint (maximum alpha around 80)
                alpha_val = int(100 * (1.0 - (i / 10.0)))
                pygame.draw.circle(
                    self.image,
                    (255, 180, 0, alpha_val),  # Golden yellow transparent glow
                    (50, 50),
                    (i + 1) * 5,
                )
            # Solid cores in the center
            pygame.draw.circle(self.image, (255, 0, 0), (50, 50), 25)
            pygame.draw.circle(self.image, (255, 127, 0), (50, 50), 17.5)
            pygame.draw.circle(self.image, (255, 255, 0), (50, 50), 10)
            pygame.draw.circle(self.image, (255, 255, 200), (50, 50), 2.5)

            # Rotate the visual image to face the direction it is flying
            angle = math.degrees(math.atan2(-self.direction.y, self.direction.x))
            self.image = pygame.transform.rotate(self.image, angle)

        self.rect = self.image.get_rect(center=self.pos)

    def update(self, targets_group):
        # 2. Move the precise float position forward
        self.pos += self.direction * self.speed

        # 3. Snap the integer pixel rect to our precise float position
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        # 4. Check for screen boundaries (leaves the interface)
        if (
            self.rect.right < 0
            or self.rect.left > game_state.W
            or self.rect.bottom < 0
            or self.rect.top > game_state.H
        ):
            self.kill()  # Safely erases the sprite from all groups
            return

        # 5. Check for target collisions using Pygame's sprite collisions
        hit_list = pygame.sprite.spritecollide(self, targets_group, False)
        for target in hit_list:
            if target != self.is_from:
                # Deduct damage if targets have health
                if hasattr(target, "hp"):
                    if self.kind.strip().lower() == "fire":
                        target.hp -= 2  # The fire projectile should do 2 damage!
                        game_state.screen_shake = max(
                            game_state.screen_shake, 0.5
                        )  # Small dynamic explosion shake
                    else:
                        target.hp -= game_state.player_group.sprite.dmg
                self.kill()  # Destroy projectile upon impacting a valid target
                if self.kind == "fire":
                    game_state.effects_group.add(
                        effects.Pop(
                            self.pos.x, self.pos.y, 30, self.zone, (255, 180, 0)
                        )
                    )
                break
