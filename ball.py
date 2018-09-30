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

        # Load the sushi image and set its rect attribute.
        self.image = pygame.image.load('images/sushi.png')
        self.rect = self.image.get_rect()

        # Start each new sushi in a random location towards the screen's center
        self.rect.centerx = random.randint(400, 800)
        self.rect.centery = random.randint(300, 500)

        # Store the sushi's exact position.
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        # Store the sushi's direction and speed
        self.dx = 1
        self.dy = 2

    def blitme(self):
        """Draw the sushi at its current location."""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return true if the sushi is at the edge of screen."""
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
        """Move the sushi left or right."""
        '''
        self.centerx += (self.ai_settings.sushi_speed_factor * self.ai_settings.fleet_direction)
        self.rect.centerx = self.centerx
        '''
        self.centerx += self.dx * self.ai_settings.sushi_speed_factor
        self.rect.centerx = self.centerx

        self.centery += self.dy * self.ai_settings.sushi_speed_factor
        self.rect.centery = self.centery