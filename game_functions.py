import sys
from time import sleep
import pygame
from ball import Ball


def check_high_score(stats, sb):
    # Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_control_events(ai_settings, screen, stats, sb, play_button, u_p_b, u_p_t, u_p_r, a_p_b, a_p_t, a_p_l, sushi_ball):
    # Respond to keypress and mouse events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, u_p_b, u_p_t, u_p_r, a_p_b, a_p_t, a_p_l)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, u_p_b, u_p_t, u_p_r, a_p_b, a_p_t, a_p_l)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, u_p_b, u_p_t, u_p_r, a_p_b, a_p_t, a_p_l, sushi_ball, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, u_p_b, u_p_t, u_p_r, a_p_b, a_p_t, a_p_l, sushi_ball, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_sushis()

        # Empty the list of aliens.
        sushi_ball.empty()

        # Create a new fleet and center the ship.
        create_sushi(ai_settings, screen, sushi_ball)


def update_screen(ai_settings, screen, stats, sb, u_p_b, u_p_t, u_p_r, a_p_b, a_p_t, a_p_l, sushi_ball, play_button):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    u_p_b.blitme()
    u_p_t.blitme()
    u_p_r.blitme()
    a_p_b.blitme()
    a_p_t.blitme()
    a_p_l.blitme()
    sushi_ball.draw(screen)

    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def check_keydown_events(event, ai_settings, screen, u_p_b, u_p_t, u_p_r, a_p_b, a_p_t, a_p_l):
    """Respond to key presses."""
    if event.key == pygame.K_RIGHT:
        u_p_b.moving_right = True
        u_p_t.moving_right = True
    elif event.key == pygame.K_LEFT:
        u_p_b.moving_left = True
        u_p_t.moving_left = True
    elif event.key == pygame.K_UP:
        u_p_r.moving_up = True
    elif event.key == pygame.K_DOWN:
        u_p_r.moving_down = True
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, u_p_b, u_p_t, u_p_r, a_p_b, a_p_t, a_p_l):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        u_p_b.moving_right = False
        u_p_t.moving_right = False
    elif event.key == pygame.K_LEFT:
        u_p_b.moving_left = False
        u_p_t.moving_left = False
    elif event.key == pygame.K_UP:
        u_p_r.moving_up = False
    elif event.key == pygame.K_DOWN:
        u_p_r.moving_down = False


def check_paddle_sushi_collisions(ai_settings, screen, stats, sb, sushi, bullets): # TODO Coverage - is used?
    """Respond to paddle-sushi collisions."""
    # Generate a collision list
    collisions = pygame.sprite.groupcollide(bullets, sushi, True, True)

    if collisions:
        for sushi in collisions.values():
            stats.score += ai_settings.alien_points * len(sushi)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(sushi) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_sushi(ai_settings, screen, sushi)


def create_sushi(ai_settings, screen, sushi_balls):
    """Create and place a sushi piece."""
    sushi = Ball(ai_settings, screen)
    sushi_balls.add(sushi)


def check_sushi_at_edges(ai_settings, screen, stats, sb, sushis):
    for sushi in sushis.sprites():
        if sushi.check_edges():
            # Respond appropriately if any sushi have reached an edge.
            if stats.sushis_left > 0:

                if sushi.rect.centerx > 600:
                    stats.ai_score += ai_settings.alien_points
                    print("AI scores!")
                elif sushi.rect.centerx < 600:
                    stats.user_score += ai_settings.alien_points
                    print("User scores!")
                elif stats.last_hit == "NULL":
                    print("Nobody scores!")

                # Decrement remaining sushi
                stats.sushis_left -= 1

                stats.last_hit = "NULL"

                # Update scoreboard.
                sb.prep_sushis()

                # Empty the list of sushi
                sushis.empty()

                # Create new sushi
                create_sushi(ai_settings, screen, sushis)

                # Pause
                sleep(0.5)

            else:
                stats.game_active = False
                pygame.mouse.set_visible(True)


def change_sushi_direction(ai_settings, sushi_pieces):
    """Change the sushi's direction."""
    for sushi in sushi_pieces.sprites():
        if sushi.dx > 0 and sushi.dy > 0:       # To the right and down
            sushi.dy *= -1
        elif sushi.dx > 0 and sushi.dy < 0:     # To the right and up
            sushi.dx *= -1
        elif sushi.dx < 0 and sushi.dy > 0:     # To the left and down
            sushi.dx *= -1
        elif sushi.dx < 0 and sushi.dy < 0:     # To the left and up
            sushi.dy *= -1



def paddle_hit(ai_settings, screen, stats, sb, paddle, sushis):
    # Respond to a paddle being hit by sushi
    if paddle.paddle_type == "USER":
        stats.last_hit = "USER"
        print("User hits")
    elif paddle.paddle_type == "AI":
        stats.last_hit = "AI"
        print("AI hits")
    change_sushi_direction(ai_settings, sushis)


def check_match_events(ai_settings, screen, stats, sb, paddles, sushi_ball):
    # Check if the sushi is at an edge
    check_sushi_at_edges(ai_settings, screen, stats, sb, sushi_ball)

    # Look for sushi-paddle collisions.
    for paddle in paddles:
        if pygame.sprite.spritecollideany(paddle, sushi_ball):
            paddle_hit(ai_settings, screen, stats, sb, paddle, sushi_ball)


def ai_play(a_p_b, a_p_t, a_p_l, sushi):
    for piece in sushi.sprites():
        if piece.centery < a_p_l.rect.centery:
            a_p_l.moving_up = True
        else:
            a_p_l.moving_up = False

        if piece.centery > a_p_l.rect.centery:
            a_p_l.moving_down = True
        else:
            a_p_l.moving_down = False

        if piece.centerx < a_p_t.rect.centerx:
            a_p_t.moving_left = True
            a_p_b.moving_left = True
        else:
            a_p_t.moving_left = False
            a_p_b.moving_left = False

        if piece.centerx > a_p_t.rect.centerx and a_p_t.rect.right < 600:
            a_p_t.moving_right = True
            a_p_b.moving_right = True
        else:
            a_p_t.moving_right = False
            a_p_b.moving_right = False