import pygame
from pygame import Vector2, sprite
import sys
import random

from coizera import events
from coizera import pubsub

main_mod = sys.modules["__main__"]


class Player(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.pos = Vector2(
            random.randint((main_mod.W // 2) - 100, (main_mod.W // 2) + 100),
            random.randint((main_mod.H // 2) - 100, (main_mod.H // 2) + 100),
        )
        self.rect = self.image.get_rect(center=self.pos)
        self.vel = Vector2(0, 0)
        self.speed = 2
        self.pitems = []
        self.holding = None
        self.dmg = 0  # Starts at 0, dynamically set by holding weapon
        self.max_hp = 20
        self.hp = self.max_hp
        self.attacked = 0
        self.target_hp = 20
        self.dead = False  # Track the dead state inside the Player object

        pygame.draw.rect(self.image, (255, 255, 0), (0, 0, 40, 40), border_radius=10)
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, 40, 40), 5, 10)
        pubsub.event_bus.subscribe(events.PLAYER_TAKES_DAMAGE, self.on_damage_taken)

    def on_damage_taken(self, event: events.PlayerTakesDamage):
        if self.attacked <= 0:
            self.target_hp = self.hp - event.damage
            self.attacked = 30
            pubsub.event_bus.publish(events.SCREEN_SHAKE, events.ScreenShake(intensity=3))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.vel.y -= self.speed
        if keys[pygame.K_a]:
            self.vel.x -= self.speed
        if keys[pygame.K_s]:
            self.vel.y += self.speed
        if keys[pygame.K_d]:
            self.vel.x += self.speed

        if (
            keys[pygame.K_1]
            and len(main_mod.weapons) > 0
            and main_mod.weapons[0] != "empty"
        ):
            self.holding = 0
        if (
            keys[pygame.K_2]
            and len(main_mod.weapons) > 1
            and main_mod.weapons[1] != "empty"
        ):
            self.holding = 1

        self.vel *= 0.8
        self.pos += self.vel
        self.rect.center = self.pos

        # --- ZONE BOUNDARY BLOCKING LOGIC ---
        if main_mod.zone == "base":
            # Only allowed to exit past the right edge (rect.left can cross past W)
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > main_mod.H:
                self.rect.bottom = main_mod.H
            self.pos.update(self.rect.center)

        elif main_mod.zone == "forest":
            # Only allowed to exit past the left edge (rect.right can cross past 0)
            if self.rect.right > main_mod.W:
                self.rect.right = main_mod.W
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > main_mod.H:
                self.rect.bottom = main_mod.H
            self.pos.update(self.rect.center)

        elif main_mod.zone in ["mine1", "mine2", "The Outer Realm"]:
            # Completely blocked on all 4 sides of the screen
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > main_mod.W:
                self.rect.right = main_mod.W
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > main_mod.H:
                self.rect.bottom = main_mod.H
            self.pos.update(self.rect.center)

        # Handle passive health regeneration
        if self.attacked > 0:
            self.attacked -= 1
        elif self.attacked <= 0 and self.target_hp < self.max_hp:
            # 1. ALWAYS modify target_hp instead of hp for smooth systems
            self.target_hp += 0.01
            if self.target_hp > self.max_hp:
                self.target_hp = self.max_hp

        # 2. Smoothly slide current hp toward target_hp
        self.hp = self.hp + (self.target_hp - self.hp) * 0.2

        # Handle death state
        if self.hp <= 0:
            self.dead = True
            self.dead_timer = 180
