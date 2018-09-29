import pygame
from pygame.sprite import Sprite


class Paddle(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position."""
        super(Paddle, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Get its rect
        self.image = pygame.image.load('images/paddle_h.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def set_user_top_paddle(self):
        self.rect.centerx = 925
        self.center = float(self.rect.centerx)
        self.rect.top = self.screen_rect.top
        self.yval = float(self.rect.centery)

    def set_ai_top_paddle(self):
        self.rect.centerx = 300
        self.center = float(self.rect.centerx)
        self.rect.top = self.screen_rect.top
        self.yval = float(self.rect.centery)

    def set_user_bottom_paddle(self):
        self.rect.centerx = 925
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom
        self.yval = float(self.rect.centery)

    def set_ai_bottom_paddle(self):
        self.rect.centerx = 300
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom
        self.yval = float(self.rect.centery)

    def set_user_right_paddle(self):
        self.image = pygame.image.load('images/paddle_v.png')
        self.rect.centerx = 1225
        self.center = 1225
        self.yval = 350

    def set_ai_left_paddle(self):
        self.image = pygame.image.load('images/paddle_v.png')
        self.rect.centerx = 75
        self.center = 75
        self.yval = 350

    def update(self):
        """Update the paddle's position based on the movement flags."""
        # Update the paddles's center value, not the rect.
        if self.moving_right and self.rect.right < 1150:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 600:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 50:
            self.yval -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < 650:
            self.yval += self.ai_settings.ship_speed_factor

        # Update the rect object from self.center.
        self.rect.centerx = self.center
        self.rect.centery = self.yval

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)