import pygame
from pygame.sprite import Sprite
import random


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
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.dx = random.randint(0,1)
        self.dy = random.randint(0,1)

        # Store the sushi's exact position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


    def blitme(self):
        """Draw the sushi at its current location."""
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
        """Move the sushi left or right."""
        self.x += self.dx
        self.y += self.dy
        self.rect.x = self.x
        self.rect.y = self.y