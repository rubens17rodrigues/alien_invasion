import sys
from time import sleep

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

def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, 
                              aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats,
                      play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Inicia um novo jogo quando o jogador clica em play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        # Oculta o cursor do mouse 
        pygame.mouse.set_visible(False)

        # Reinicia os dados estatísticos do jogo
        stats.reset_stats()
        stats.game_active = True

        # Esvazia a lista de aliens e de projéteis
        aliens.empty()
        bullets.empty()

        # Cria uma nova frota e centraliza a nave
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button):
    """Atualiza as imagens na tela e alterna para a nova tela."""
    # Redesenha a tela a cada passagem pelo laço
    screen.fill(ai_settings.bg_color)

    #Redesenha todos os projéteis
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Desenha o botão play se o jogo estiver inativo
    if not stats.game_active:
        play_button.draw_button()

    # Deixa a tela mais recente visível
    pygame.display.flip()

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """Atualiza a posição dos projéteis e se livra dos antigos ."""

    bullets.update()

    # Remove os projéteis que ultrapassam a tela
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """Responde a colisões entre projéteis e aliens."""
    # Verifica se algum projetil atingiu os aliens e os removem 
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        # Destroi os projéteis existentes e cria uma nova frota
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


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

def check_fleet_edges(ai_settings, aliens):
    """Respode se algum alien alcançou a borda."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
def change_fleet_direction(ai_settings, aliens):
    """Faz toda a frota descer e muda a sua direção."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Responde ao fato da nave ter sido atingida por um alien."""
    if stats.ships_left > 0:
        # Decrementa ships_left
        stats.ships_left -= 1

        # Esvazia a lista de aliens e de projéteis
        aliens.empty()
        bullets.empty()

        # Cria uma nova frota e centraliza a nave
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Faz uma pausa
        sleep(0.5)

    else:
        pygame.mouse.set_visible(True)
        stats.game_active = False

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Verifica se algum alien alcançou a parte inferior da tela."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Trata esse caso igual quando a nave é atingida.
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """Atualiza as posições de todos os aliens."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Verifica colisão da nave e dos aliens.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    # Verifica se há algum alien que atingiu a parte inferior da tela
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
