import pygame
import random
from pygame.sprite import Sprite


class Ball(Sprite):
    """A class to represent a sushi ball."""

    def __init__(self, ai_settings, screen):
        """Initialize the sushi ball and set its starting position."""
        super(Ball, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the suhsi image and set its rect attribute.
        self.image = pygame.image.load('images/sushi.png')
        self.rect = self.image.get_rect()

        # Start each new sushi near the top left of the screen.
        self.rect.x = random.randint(400,800)
        self.rect.y = random.randint(300,500)

        # Store the alien's exact position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return true if a sushi is at the edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        elif self.rect.top <= 0:
            return True
        elif self.rect.bottom >= screen_rect.bottom:
            return True

    def update(self):
        """Move the alien right or left."""
        self.x += (self.ai_settings.sushi_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x