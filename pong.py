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
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Sushi Pong')

    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")

    # Make the menu.
    menu_font = pygame.font.SysFont('Arial', 40)
    game_title = menu_font.render("SUSHI PONG AI -- NO WALLS", False, (0, 0, 0))

    # Make the net.
    net = pygame.image.load('images/net.png')
    netrect = net.get_rect()
    screen_rect = screen.get_rect()
    netrect.center = screen_rect.center

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a group of sushi_balls, user paddles and ai paddles.
    sushi_ball = Group()
    paddles = Group()

    u_p_b = Paddle(ai_settings, screen)
    u_p_b.set_user_bottom_paddle()
    paddles.add(u_p_b)

    u_p_t = Paddle(ai_settings, screen)
    u_p_t.set_user_top_paddle()
    paddles.add(u_p_t)

    u_p_r = Paddle(ai_settings, screen)
    u_p_r.set_user_right_paddle()
    paddles.add(u_p_r)

    a_p_b = Paddle(ai_settings,screen)
    a_p_b.set_ai_bottom_paddle()
    paddles.add(a_p_b)

    a_p_t = Paddle(ai_settings, screen)
    a_p_t.set_ai_top_paddle()
    paddles.add(a_p_t)

    a_p_l = Paddle(ai_settings, screen)
    a_p_l.set_ai_left_paddle()
    paddles.add(a_p_l)

    gf.create_sushi(ai_settings, screen, sushi_ball)

    # Start the main loop for the game.
    while True:

        gf.check_control_events(ai_settings, screen, stats, sb, play_button, u_p_b, u_p_t, u_p_r, a_p_b, a_p_t, a_p_l, sushi_ball, game_title)

        if stats.game_active:
            # Move the paddles, sushi
            gf.ai_play(a_p_b, a_p_t, a_p_l, sushi_ball)
            paddles.update()
            sushi_ball.update()
            # Check for collisions between sushi, screen edges and padles
            gf.check_match_events(ai_settings, screen, stats, sb, paddles, sushi_ball)

        gf.update_screen(ai_settings, screen, stats, sb, u_p_b, u_p_t, u_p_r, a_p_b, a_p_t, a_p_l, sushi_ball, play_button, game_title, net, netrect)


run_game()