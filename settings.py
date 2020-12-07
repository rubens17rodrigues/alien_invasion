class Settings():
    """Uma classe para armazenar todas as configurações do jogo."""

    def __init__(self):
        """Inicializa as configurações estáticas do jogo."""
        # Configurações da tela
        self.screen_width = 1320
        self.screen_height = 730
        self.bg_color = ('grey')

        # Configurações da nave
        self.ship_limit = 3

        # Configurações dos projéteis
        self.bullet_width = 130
        self.bullet_height = 15
        self.bullet_color = ('blue')
        self.bullets_allowed = 30

        # Configurações dos aliens
        self.fleet_drop_speed = 10

        # A taxa com que a velocidade do jogo aumenta
        self.speedup_scale = 1.3

        # A taxa com que os pontos para cada alien aumentam
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inicializa as configurações que mudam no decorrer do jogo."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet_direction igual a 1 representa a direita; -1 esquerda
        self.fleet_direction = 1

        # Pontuação
        self.alien_points = 10

    def increase_speed(self):
        """Aumenta as configurações de velocidade."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points *= int(self.alien_points * self.score_scale)
