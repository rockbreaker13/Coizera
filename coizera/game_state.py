import pygame
from pygame import sprite

from coizera import player
from coizera.weapon import Weapon

# Pygame setup
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Display dimensions
info = pygame.display.Info()
W, H = info.current_w - 80, info.current_h - 80
screen = pygame.display.set_mode((W, H), vsync=True, flags=pygame.RESIZABLE)

# Sprite Groups
player_group = sprite.GroupSingle(player.Player())
items_group = sprite.Group()
buildings_group = sprite.Group()
weapon_group = sprite.GroupSingle(Weapon())
enemy_group = sprite.Group()
effects_group = sprite.Group()
projectiles_group = sprite.Group()

# Global state
zone = "base"
screen_shake = 0.0
inventory = [
    "empty", "empty", "empty", "empty", "empty",
    "empty", "empty", "empty", "empty", "empty",
]
weapons = ["empty", "empty"]
total_items = 0
