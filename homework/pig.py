import pygame
from pygame.sprite import Sprite
from random import randint

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

        self.counter = 0
        self.direction = 0
        self.duration = randint(60, 140)

    def direction_changer(self, instant_change = 1):
        """Изменяте направление движения свиньи"""
        if self.counter == 0:
            self.direction = randint(1, 4)

        if self.direction == 1:
            self.rect.y += 1
        elif self.direction == 2:
            self.rect.x += 1
        elif self.direction == 3:
            self.rect.y -= 1
        elif self.direction == 4:
            self.rect.x -= 1

        self.counter +=1
        if self.counter == self.duration or instant_change == 0:
            self.counter = 0
            self.duration = randint(60, 140)
            instant_change = 1
