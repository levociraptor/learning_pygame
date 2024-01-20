class GameStats():
    """Отслеживание статистики для игры Alien Invasion"""

    def __init__(self, ai_game):
        """Инициализирует статистику"""
        self.settings = ai_game.settings
        self.reset_stats()

        # Игра запускается в неактивном состоянии
        self.game_active = True

        # Рекорд не должен сбрасываться
        with open("record.txt", "r") as rec:
            record = rec.read()
        self.high_score = int(record)

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры"""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1



