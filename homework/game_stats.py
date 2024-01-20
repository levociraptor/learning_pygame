class Game_stats():
    """Статистика для игры"""

    def __init__(self):
        """Инициалищирует статистику"""
        self.reset_stats()

        # Игра запускается в неактивном режиме
        self.game_active = False

        # Общий счет игрока
        self.score = 0

        # Количество собранных звезд персонажем в раунде
        self.person_star_score = 0

        # Количесво собранных звезд свиньями в раунде
        self.pigs_star_score = 0

        # Количество жизней у персонажа
        self.person_hp = 3

    def reset_stats(self):
        self.person_star_score = 0
        self.pigs_star_score = 0
        self.person_hp = 3

    def reset_stats_completely(self):
        self.score = 0


