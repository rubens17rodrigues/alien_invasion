import sys

import pygame
from bullet import Bullet

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

def update_screen(ai_settings, screen, ship, bullets):
    """Atualiza as imagens na tela e alterna para a nova tela."""
    # Redesenha a tela a cada passagem pelo laço
    screen.fill(ai_settings.bg_color)
    ship.blitme()

    #Redesenha todos os projéteis
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Deixa a tela mais recente visível
    pygame.display.flip()

def update_bullets(bullets):
    """Atualiza a posição dos projéteis e se livra dos antigos ."""

    bullets.update()

    # Remove os projéteis que ultrapassam a tela
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


