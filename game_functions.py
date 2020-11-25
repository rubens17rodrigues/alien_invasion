import sys

import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Responde a pressionamento de tecla."""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_UP or event.key == pygame.K_w:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
    """Dispara u m projétil se  o limite n for atingido"""

    # Cria um novo projétil e o adiciona ao grupo de projéteis
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    """Responde a soltudas de tecla."""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = False
    elif event.key == pygame.K_UP or event.key == pygame.K_w:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        ship.moving_down = False

def check_events(ai_settings, screen, ship, bullets):
    """Responde a enventos de pressionamento de teclas e de mouse."""
    for event in pygame.event.get():
        # Sai do jogo
        if event.type == pygame.QUIT:
            sys.exit()

        # Controla os movimentos da nave 
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings,  screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def update_screen(ai_settings, screen, ship, aliens, bullets):
    """Atualiza as imagens na tela e alterna para a nova tela."""
    # Redesenha a tela a cada passagem pelo laço
    screen.fill(ai_settings.bg_color)

    #Redesenha todos os projéteis
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Deixa a tela mais recente visível
    pygame.display.flip()

def update_bullets(bullets):
    """Atualiza a posição dos projéteis e se livra dos antigos ."""

    bullets.update()

    # Remove os projéteis que ultrapassam a tela
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """Determina o número de alienígenas que cabem em uma linha."""
    available_space_x = ai_settings.screen_width - 2* alien_width
    number_aliens_x = int (available_space_x /(2* alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determina o número de linhas com aliens q cabem na tela."""
    available_space_y = (ai_settings.screen_height -
                         (3*alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # Cria um alienígena e o posiciona na linha
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2* alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Cria uma frota completa de aliens."""
    # Cria um alienigena e calcula a qtd em uma linha
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(
        ai_settings,alien.rect.width)
    number_rows = get_number_rows(
        ai_settings, ship.rect.height, alien.rect.height)

    # Cria a frota de aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


