import pygame
from pygame import sprite, Vector2
import math
import random


class Pop(sprite.Sprite):
    def __init__(self, x, y, r, zone, c=(255, 255, 255)):
        super().__init__()
        self.radius = r
        self.pos = Vector2(x, y)
        self.zone = (
            zone  # Added to make sure we only sort and render in the current zone
        )
        self.color = c
        self.v = 5

        # 1. Initialize empty sprite attributes required for Y-sorting compatibility
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)
        self.update_image()

    def update_image(self):
        """Creates a dynamic local surface matching the expanding pop circle."""
        size = int(self.radius * 2)
        if size <= 0:
            self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
            self.rect = self.image.get_rect(center=self.pos)
            return

        # 2. Create a clean, transparent surface matching the size of the pop boundary
        self.image = pygame.Surface((size, size), pygame.SRCALPHA).convert_alpha()

        # Draw the circle centered locally (at center, center) instead of globally
        center = size // 2
        pygame.draw.circle(
            self.image,
            self.color,
            (center, center),
            int(self.radius),
            max(1, int(self.radius // 5)),
        )

        # 3. Keep the drawing rect centered perfectly on our logical position vector
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.radius += self.v
        self.v -= 1
        if self.radius <= 1:
            self.kill()
        else:
            self.update_image()


class Message(pygame.sprite.Sprite):
    def __init__(self, message, color, zone, pos=None, font_size=50, duration=180):
        super().__init__()

        # Default to screen center if no position is given
        if pos is None:
            # Replace main.W//2 with your actual screen width variable if needed
            pos = pygame.math.Vector2(pygame.display.get_surface().get_width() // 2, 50)

        # 1. Set up the font (Consolas, bold is optional but looks better when big)
        self.font = pygame.font.SysFont("Consolas", font_size, bold=True)
        self.zone = zone
        # 2. Render the base text surface
        self.text_color = color
        self.text_string = message
        self.base_image = self.font.render(self.text_string, True, self.text_color)

        # Create a copy that we will apply transparency changes to
        self.image = self.base_image.copy()

        # 3. Handle centering perfectly using rect
        self.rect = self.image.get_rect(center=(pos.x, pos.y))

        # 4. Timing and Fading Variables (duration is measured in frames)
        self.duration = duration
        self.timer = 0

        # Define how long the fade-in and fade-out take (e.g., 30 frames each)
        self.fade_duration = min(30, duration // 3)

        # Start invisible
        self.alpha = 0
        self.image.set_alpha(self.alpha)

    def update(self):
        self.timer += 1

        # Check if the message's lifespan is over
        if self.timer >= self.duration:
            self.kill()  # Automatically removes it from all sprite groups
            return

        # Calculate Alpha based on the current frame time
        if self.timer < self.fade_duration:
            # Fading In: Alpha goes from 0 to 255
            self.alpha = int((self.timer / self.fade_duration) * 255)
        elif self.timer > (self.duration - self.fade_duration):
            # Fading Out: Alpha goes from 255 down to 0
            frames_left = self.duration - self.timer
            self.alpha = int((frames_left / self.fade_duration) * 255)
        else:
            # Fully Visible state
            self.alpha = 255

        # Apply the updated alpha to a fresh copy of the text surface
        self.image = self.base_image.copy()
        self.image.set_alpha(self.alpha)


class Twinkle(pygame.sprite.Sprite):
    def __init__(self, pos, size, zone, color=(255, 255, 255)):
        super().__init__()
        self.size = size
        self.color = color
        self.pos = pygame.Vector2(pos)
        self.zone = zone

        # Create a transparent surface large enough to fit the star flare
        self.image = pygame.Surface(
            (size * 2, size * 2), pygame.SRCALPHA
        ).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)

        # Set a randomized lifespan so multiple twinkles don't pulse at the exact same time
        self.max_life = random.randint(20, 40)
        self.life = self.max_life

    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()  # Automatically delete the particle when it finishes twinkly life!
            return

        # Use a sine wave to calculate a smooth fade-in and fade-out transparency curve
        progress = (self.max_life - self.life) / self.max_life
        alpha = int(255 * math.sin(progress * math.pi))
        alpha = max(0, min(255, alpha))

        # Clear old canvas frame
        self.image.fill((0, 0, 0, 0))
        center = self.size

        # Combine base RGB colors with dynamic alpha
        r, g, b = self.color[:3]
        color_with_alpha = (r, g, b, alpha)

        # Draw a beautiful 4-pointed glowing cross shape
        pygame.draw.line(
            self.image, color_with_alpha, (center, 0), (center, self.size * 2), 2
        )
        pygame.draw.line(
            self.image, color_with_alpha, (0, center), (self.size * 2, center), 2
        )

        # Draw a diamond-shaped core in the middle of the flare
        pygame.draw.polygon(
            self.image,
            color_with_alpha,
            [
                (center, center - self.size // 3),
                (center + self.size // 3, center),
                (center, center + self.size // 3),
                (center - self.size // 3, center),
            ],
        )

        # Center the rect back to the absolute coordinate
        self.rect = self.image.get_rect(center=self.pos)
