import pygame
from pygame import sprite
import math

from coizera import game_state
from coizera import long_init_stuff
from coizera.projectile import Projectile


class Weapon(sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Store a clean, unrotated master copy of the weapon
        self.original_image = pygame.Surface((30, 100), pygame.SRCALPHA).convert_alpha()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()

        # Smooth lerp state variables
        self.is_swinging = False
        self.swing_progress = 0.0  # Runs from 0.0 (start) to 1.0 (end)
        self.swing_angle = 0
        self.swing_speed = 0.2  # Setup default swing speed to prevent NameErrors

        # Visual Trace/Slash Trail variables
        self.trail = []
        self.trail_surf = pygame.Surface((game_state.W, game_state.H), pygame.SRCALPHA)

    def update(self):
        # 1. Safely check if a weapon is active, search our WEAPONS dictionary list, and transfer data
        holding_idx = game_state.player_group.sprite.holding
        if (
            holding_idx is not None
            and holding_idx < len(game_state.weapons)
            and game_state.weapons[holding_idx] != "empty"
        ):
            weapon_name = game_state.weapons[holding_idx].strip().lower()
            # Match active weapon name inside our new WEAPONS list of dictionaries
            weapon_data = next(
                (w for w in long_init_stuff.WEAPONS if w["name"] == weapon_name),
                None,
            )
            if weapon_data:
                # Transfer drawn image
                self.original_image = weapon_data["image"]
                # Dynamically set player damage according to held weapon stats!
                game_state.player_group.sprite.dmg = weapon_data["dmg"]

                # --- CHECK FOR SPECIAL EFFECTS & APPLY THEM ---
                # Safe lookup of the "special" dictionary (defaults to empty dict if missing)
                special_effects = weapon_data.get("special", {})

                # FIXED: Apply modifiers safely without overwriting each other
                if "speed" in special_effects:
                    self.swing_speed = special_effects["speed"]
                elif "slow" in special_effects:
                    self.swing_speed = special_effects["slow"]
                else:
                    self.swing_speed = 0.12

                self.color = special_effects.get("fire", (255, 255, 255))

            else:
                # If nothing is held, use a completely transparent surface so nothing draws
                self.original_image = pygame.Surface(
                    (1, 1), pygame.SRCALPHA
                ).convert_alpha()
                game_state.player_group.sprite.dmg = 0
                self.swing_speed = (
                    0.2  # Reset back to default speed when weapon data is invalid
                )
        else:
            # If nothing is held, use a completely transparent surface so nothing draws
            self.original_image = pygame.Surface(
                (1, 1), pygame.SRCALPHA
            ).convert_alpha()
            game_state.player_group.sprite.dmg = 0
            self.swing_speed = 0.2  # Reset back to default speed when no weapon is held

        # 2. Get the angle pointing directly to the mouse
        mouse_pos = pygame.mouse.get_pos()
        player_pos = game_state.player_group.sprite.pos
        direction = pygame.math.Vector2(mouse_pos) - player_pos
        if game_state.weapon_group:
            pass
        if direction.length() > 0:
            # Trigonometry to get base angle (0 is East, 90 is North)
            base_angle = math.degrees(math.atan2(-direction.y, direction.x))
        else:
            base_angle = 90.0

        # 3. Proper Progress-Based Lerp Swing Logic
        if pygame.mouse.get_pressed()[0] and not self.is_swinging:
            self.is_swinging = True
            self.swing_progress = 0.0
            self.trail.clear()  # Refresh trail on active click

            # --- FIXED: Only fire projectiles if holding the Inferno weapon ---
            holding_idx = game_state.player_group.sprite.holding
            if (
                holding_idx is not None
                and holding_idx < len(game_state.weapons)
                and game_state.weapons[holding_idx].strip().lower() == "inferno"
            ):
                for d in range(3):
                    game_state.projectiles_group.add(
                        Projectile(
                            game_state.player_group,
                            "fire",
                            game_state.player_group.sprite.pos.copy(),
                            10,
                            direction,
                            game_state.zone,
                        )
                    )

        if self.is_swinging:
            # Smoothly transition progress towards 1.0 (Uses the updated dynamic swing_speed!)
            self.swing_progress += (1.0 - self.swing_progress) * self.swing_speed
            # Map progress to our swing angle (+45 to -45 gives a clean 90-degree wedge)
            self.swing_angle = 90 + self.swing_progress * (-90 - 90)

            # Once we are basically finished with the lerp, reset
            if self.swing_progress >= 0.98:
                self.is_swinging = False
                self.swing_progress = 0.0
                self.trail.clear()  # Erase trail upon swing completion
        else:
            self.swing_progress += (1.0 - self.swing_progress) * 0.25
            # Map progress to our swing angle
            self.swing_angle = -90 + self.swing_progress * 180

        # 4. Combine base mouse angle with our swing angle offset
        final_angle = base_angle + self.swing_angle

        # 5. Rotate the newly transferred original_image copy
        self.image = pygame.transform.rotate(self.original_image, final_angle - 90)

        # 6. Push the sword forward in front of the player
        rad = math.radians(final_angle)
        offset_vector = pygame.math.Vector2(math.cos(rad), -math.sin(rad))
        # Adjust '75' to change how far out from the player the sword is positioned
        sword_distance = 75
        self.rect = self.image.get_rect(
            center=player_pos + offset_vector * sword_distance
        )

        # 7. Record position history using our substepping logic!
        if self.is_swinging:
            hilt_pos = player_pos + offset_vector * 35
            tip_pos = player_pos + offset_vector * 125
            self.update_trail(hilt_pos, tip_pos)

    def update_trail(self, hilt_pos, tip_pos):
        """Generates smooth, intermediate points between frames using vector substepping."""
        if self.is_swinging:
            # If we have a previous position, interpolate intermediate steps
            if self.trail:
                last_hilt, last_tip = self.trail[-1]
                substeps = 4  # Number of segments to split the gap into
                for step in range(1, substeps + 1):
                    t = step / substeps
                    # Linearly interpolate (lerp) hilt and tip positions
                    sub_hilt = last_hilt.lerp(hilt_pos, t)
                    sub_tip = last_tip.lerp(tip_pos, t)
                    self.trail.append((sub_hilt, sub_tip))
            else:
                self.trail.append((hilt_pos, tip_pos))

            # Maintain maximum length history boundary (increased because we have substeps now!)
            if len(self.trail) > 30:
                self.trail.pop(0)

    def draw_trail(self, surface, offset_x=0, offset_y=0):
        """Draws the fading sword trace on the main screen with substepping smoothing."""
        if not self.trail or len(self.trail) < 2:
            return

        # Dynamically resize the trail surface if it doesn't match the current display window size
        target_size = surface.get_size()
        if self.trail_surf.get_size() != target_size:
            self.trail_surf = pygame.Surface(target_size, pygame.SRCALPHA)

        self.trail_surf.fill((0, 0, 0, 0))  # Clear transparency buffer

        # 1. Draw the main fading body of the slash
        for i in range(len(self.trail) - 1):
            hilt_curr, tip_curr = self.trail[i]
            hilt_next, tip_next = self.trail[i + 1]
            # Fading alpha
            alpha = int(180 * (i / len(self.trail)))
            color = (self.color[0], self.color[1], self.color[2], alpha)
            quad_points = [hilt_curr, tip_curr, tip_next, hilt_next]
            pygame.draw.polygon(self.trail_surf, color, quad_points)

        # 2. Draw the EXTRA slash highlight right at the tip of the blade!
        if len(self.trail) >= 8:
            # Grab the last few tip positions (more points because of substepping)
            tip_points = [tip for hilt, tip in self.trail[-8:]]
            # Draw a bright, solid white line connecting the recent tips to define a sharp cutting edge
            pygame.draw.lines(
                self.trail_surf,
                (self.color[0], self.color[1], self.color[2], 200),
                False,
                tip_points,
                4,
            )

        # Blit the composite trace surface onto the main display, offset by the active screen shake values
        surface.blit(self.trail_surf, (offset_x, offset_y))
