import pygame.font
from pygame.sprite import Group

from heart import Heart

class Scoreboard():
    """Класс для вывода игровой статистики на экран"""

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # Настройки шрифта для вывода счета
        self.text_color_char = (38, 201, 135)
        self.text_color_pigs = (238, 48, 79)
        self.font = pygame.font.SysFont(None, 48)

        # Цвет фона
        self.bg_color = (255, 255, 255)

        # Подготовка изображения
        self.prep_score()
        self.prep_pig_score()
        self.prep_hearts()

    def prep_score(self):
        """Преобразует текущий счет в картинку"""
        score_str = str(self.game.game_stats.person_star_score)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color_char, self.bg_color)

        # Вывод счета на экран
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_pig_score(self):
        """Преобразует собранные свиньей звезды в картинку"""
        pigs_score_str = str(self.game.game_stats.pigs_star_score)
        self.pigs_score_image = self.font.render(pigs_score_str, True,
                                            self.text_color_pigs, self.bg_color)

        # Вывод счета свиньи на экран
        self.pigs_score_rect = self.pigs_score_image.get_rect()
        self.pigs_score_rect.left = 20
        self.pigs_score_rect.top = 20

    def prep_hearts(self):
        self.hearts = Group()
        for hp_number in range(self.game.game_stats.person_hp):
            hp = Heart(self.game)
            hp.rect.x = (self.screen_rect.width // 2) - (2 * hp.rect.width) + hp_number * hp.rect.width
            hp.rect.y = 10
            self.hearts.add(hp)
            print(hp.rect.width)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.pigs_score_image, self.pigs_score_rect)
        self.hearts.draw(self.screen)

