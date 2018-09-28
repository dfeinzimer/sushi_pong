import sys
from time import sleep
import pygame
from ball import Ball
from paddle import Paddle

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens):
    """Responds to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, mouse_x, mouse_y):
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
        aliens.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, play_button):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)

    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()

def check_keydown_events(event, ai_settings, screen, ship):
    """Respond to key presses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def get_number_sushis_x(ai_settings, alien_width):
    """Determine the number of sushi that fit in a row."""
    #available_space_x = ai_settings.screen_width - 2 * alien_width
    #number_sushis_x = int(available_space_x / (2 * alien_width))
    number_sushis_x = 1
    return number_sushis_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of sushi that fit on the screen."""
    #available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    #number_rows = int(available_space_y / (2 * alien_height))
    number_rows = 1
    return number_rows

def create_sushi(ai_settings, screen, sushi_balls, alien_number, row_number):
    """Create and place a sushi piece."""
    sushi = Ball(ai_settings, screen)
    sushi_width = sushi.rect.width
    sushi.x = sushi_width + 2 * sushi_width * alien_number
    sushi.rect.x = sushi.x
    sushi.rect.y = sushi.rect.height + 2 * sushi.rect.height * row_number
    sushi_balls.add(sushi)

def create_ai_paddles(ai_settings, screen, ai_paddles):
    """Create a full fleet of ai paddles."""
    ai_paddles_top = Paddle(ai_settings, screen)
    ai_paddles_top.y = 200
    ai_paddles_top.rect.y = ai_paddles_top.y
    ai_paddles.add(ai_paddles_top)

    user_paddles_bottom = Paddle(ai_settings, screen)
    ai_paddles.add(user_paddles_bottom)

    ai_paddles_left = Paddle(ai_settings, screen)
    ai_paddles.add(ai_paddles_left)

def create_user_paddles(ai_settings, screen, user_paddles):
    """Create a full fleet of user paddles."""
    user_paddles_top = Paddle(ai_settings, screen)
    user_paddles_top.y = 200
    user_paddles_top.rect.y = user_paddles_top.y
    user_paddles.add(user_paddles_top)

    user_paddles_bottom = Paddle(ai_settings, screen)
    user_paddles.add(user_paddles_bottom)

    user_paddles_right = Paddle(ai_settings, screen)
    user_paddles.add(user_paddles_right)

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of sushi."""
    # Create a sushi and find the number of sushi in a row.
    sushi = Ball(ai_settings, screen)
    number_sushis_x = get_number_sushis_x(ai_settings, sushi.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  sushi.rect.height)

    # Create the fleet of sushi.
    for row_number in range(number_rows):
        for alien_number in range(number_sushis_x):
            create_sushi(ai_settings, screen, aliens, alien_number,
                         row_number)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens):
    """Respond to the ship being hit by an alien."""
    if stats.sushis_left > 0:
        # Decrement sushis_left.
        stats.sushis_left -= 1

        # Update scoreboard.
        sb.prep_sushis()

        # Empty the list of aliens.
        aliens.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens):
    """
    Check if the sushi is at an edge,
      and then update the positions of all sushi in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens)