import pygame
from pygame.sprite import Sprite

class Pig(Sprite):
    """Класс представляющий свинью"""

    def __init__(self, window):
        super().__init__()
        self.screen = window.screen

        # Загрузка изображения и создание атрибута rect
        self.image = pygame.image.load("image/pig.png")
        self.rect = self.image.get_rect()

        # Новая свинья появляется в углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной горизонтальной позиции экрана
        self.x = float(self.rect.x)

        # Количество здоровья у свиньи
        self.hit_points = 7

        # Cобранные звезды
        self.collected_stars = 0
