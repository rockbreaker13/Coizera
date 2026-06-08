import pygame
from pygame import sprite

from coizera import pubsub

# Fonts init
pygame.font.init()
ui_font = pygame.font.SysFont("Consolas", 13)


class LabeledButton(sprite.Sprite):
    def __init__(self, x, y, width, height, label, event, event_data):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.event = event
        self.event_data = event_data
        self.click_cooldown = 0

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.draw_button()

    def draw_button(self, is_hovered=False):
        if is_hovered:
            color = (255, 127, 10)
        else:
            color = (10, 10, 10)

        pygame.draw.rect(self.image, ("brown"), (0, 0, self.rect.width, self.rect.height), border_radius=5)
        pygame.draw.rect(self.image, (100, 100, 100), (0, 10, self.rect.width, self.rect.height - 10), border_radius=5)
        pygame.draw.rect(self.image, color, (0, 0, self.rect.width, self.rect.height), 10, 5)

        text_surface = ui_font.render(self.label, True, (0, 0, 0))
        self.image.blit(text_surface, (15, 15))

    def update(self):
        if self.click_cooldown > 0:
            self.click_cooldown -= 1

        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)

        self.draw_button(is_hovered)

        if is_hovered and pygame.mouse.get_pressed()[0] and self.click_cooldown == 0:
            self.click_cooldown = 15
            pubsub.event_bus.publish(self.event, self.event_data)
