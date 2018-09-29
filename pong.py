import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from paddle import Paddle
import game_functions as gf


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Sushi Pong')

    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a group of sushi_balls, user paddles and ai paddles.
    u_p_b = Paddle(ai_settings, screen)
    u_p_b.set_bottom_paddle()

    u_p_t = Paddle(ai_settings, screen)
    u_p_t.set_top_paddle()

    u_p_r = Paddle(ai_settings, screen)
    u_p_r.set_right_paddle()

    sushi_ball = Group()

    # Create sushi.
    gf.create_sushi(ai_settings, screen, sushi_ball)

    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, u_p_b, u_p_t, u_p_r, sushi_ball)

        if stats.game_active:
            # Move the ship
            u_p_b.update()
            u_p_t.update()
            u_p_r.update()
            # Check for collisions between sushi, screen edges and padles
            gf.update_aliens(ai_settings, screen, stats, sb, u_p_b, u_p_t, u_p_r, sushi_ball)

        gf.update_screen(ai_settings, screen, stats, sb, u_p_b, u_p_t, u_p_r, sushi_ball, play_button)


run_game()