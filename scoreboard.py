import pygame.font
from pygame.sprite import Group

from ball import Ball

class Scoreboard():
    """A class to report scoring information."""

    def prep_sushis(self):
        """Show how much sushi remains"""
        self.sushis = Group()
        for sushi_number in range(self.stats.sushis_left):
            sushi = Ball(self.ai_settings, self.screen)
            sushi.rect.x = 10 + sushi_number * sushi.rect.width
            sushi.rect.y = 10
            self.sushis.add(sushi)

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.user_score_image, self.user_score_rect)
        self.screen.blit(self.ai_score_image, self.ai_score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        # Draw ships.
        self.sushis.draw(self.screen)

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
            self.text_color, self.ai_settings.bg_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.high_score_rect.top

    def prep_user_score(self):
        """Turn the user score into a rendered image."""
        rounded_score = int(round(self.stats.user_score, -1))
        score_str = "{:,}".format(rounded_score)
        self.user_score_image = self.font.render(score_str, True, self.text_color,
                                            self.ai_settings.bg_color)

        # Display the score at the top right of the screen.
        self.user_score_rect = self.user_score_image.get_rect()
        self.user_score_rect.right = self.screen_rect.right - 20
        self.user_score_rect.top = 80

    def prep_ai_score(self):
        """Turn the ai score into a rendered image."""
        rounded_score = int(round(self.stats.ai_score, -1))
        score_str = "{:,}".format(rounded_score)
        self.ai_score_image = self.font.render(score_str, True, self.text_color,
                                            self.ai_settings.bg_color)

        # Display the score at the top left of the screen.
        self.ai_score_rect = self.ai_score_image.get_rect()
        self.ai_score_rect.left = self.screen_rect.left + 20
        self.ai_score_rect.top = 80

    def __init__(self, ai_settings, screen, stats):
        """Initializing scorekeeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Font setting for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score images.
        self.prep_user_score()
        self.prep_ai_score()
        self.prep_high_score()
        self.prep_sushis()