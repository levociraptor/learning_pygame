import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    """Класс представляющий одну звезду"""
    def __init__(self, window):
        super().__init__()
        self.screen = window.screen

        #Загрузка изображения и создание атрибута rect
        self.image = pygame.image.load("image/star.png")
        self.rect = self.image.get_rect()

        #Новая звезда появляется в улгу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Сохранение точной горизонтальной позиции экрана
        self.x = float(self.rect.x)

