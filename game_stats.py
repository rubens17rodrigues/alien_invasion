class GameStats():
    """Armazena dados estatísticos da Invasão alien."""
    def __init__(self, ai_settings):
        """Inicializa os dados estatísticos."""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Inicia a invasão em um estado inativo
        self.game_active = False

        # A pontuação máxima n deve ser reiniciada
        try:
            with open ('high_score.txt') as file_object:
                self.high_score = int(file_object.read())
        except FileNotFoundError:
             self.high_score = 0

    def reset_stats(self):
        """Inicializa os dados estatísticos que podem mudar durante o jogo."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
