import pygame
from pygame.sprite import Sprite

class Drop(Sprite):
    """Класс представляющий одну каплю дождя"""
    def __init__(self, window):
        super().__init__()
        self.screen = window.screen

        #загрузка изображения и создания атрибута rect
        self.image = pygame.image.load("image/drop.png")
        self.rect = self.image.get_rect()

        # Новая капля появляется в улгу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Сохранение точной горизонтальной позиции экрана
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

