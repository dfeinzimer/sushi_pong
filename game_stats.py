class GameStats():
    """Track statistics for Sushi Pong"""

    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Start game in an inactive state.
        self.game_active = False

        # High score should never be reset.
        self.high_score = 0

        # Last player to hit the sushi (USER, AI or NULL)
        self.last_hit = "NULL"

    def reset_stats(self):
        # Initialize statistics that can change during the game
        self.sushis_left = self.ai_settings.ship_limit
        self.user_score = 0
        self.ai_score = 0
        self.level = 1
        self.last_hit = "NULL"

    def ai_hit(self):
        self.last_hit = "AI"

    def user_hit(self):
        self.last_hit = "USER"