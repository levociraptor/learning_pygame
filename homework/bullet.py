import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Управление снарядами"""
    def __init__(self, window):
        """Создает объект снаряда в текущей позиции корабля"""
        super().__init__()
        self.screen = window.screen
        self.color = (60, 60, 60)

        #Создание снаряда в позиции (0, 0) м назанчение правильной позиции
        self.rect = pygame.Rect(0, 0, 3, 15)
        self.rect.midtop = window.char.rect.midtop

        #Позиция снаряда в вещественном числе
        self.y = float(self.rect.y)

    def update(self):
        #обновление позции снаряда в вещственном формате
        self.y -= 2
        #Обновление позиции прямоугольника
        self.rect.y = self.y

    def draw_bullet(self):
        """Вывод снарядя на экран"""
        pygame.draw.rect(self.screen, self.color, self.rect)
