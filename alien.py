import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Uma classe q representa um único alien."""
    def __init__(self, ai_settings, screen):
        """Inicializa o alienígena e define sua posição inicial."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Carrega a imagem do alien e define seu atributo rect
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()

        #Inicia cada novo alienígena próximo a parte superior esquerda da tela

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Armazena a posição exata do alienígena
        self.x = float(self.rect.x)

    def blitme(self):
        """Desenha o alien em sua posição atual."""
        self.screen.blit(self.image, self.rect)
