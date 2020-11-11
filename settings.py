class Settings():
    """Uma classe para armazenar todas as configurações do jogo."""

    def __init__(self):
        """Inicializa as configurações do jogo."""
        # Configurações da tela
        self.screen_width = 1320
        self.screen_height = 730
        self.bg_color = ('grey')

        # Configurações da nave
        self.ship_speed_factor = 1.5
