import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Управление снарядами"""
    def __init__(self, window, bullet_direction):
        """Создает объект снаряда в текущей позиции корабля"""
        super().__init__()
        self.screen = window.screen
        self.color = (60, 60, 60)

        #Создание снаряда в позиции (0, 0) м назанчение правильной позиции
        self.rect = pygame.Rect(0, 0, 8, 8)
        self.rect.midtop = window.char.rect.midtop

        #Позиция снаряда в вещественном числе
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        #Направление снаряда
        self.bullet_direction = bullet_direction

    def update(self):
        #обновление позции снаряда в вещственном формате
        if self.bullet_direction == 1:
            self.y -= 2
        elif self.bullet_direction == 3:
            self.y += 2
        elif self.bullet_direction == 2:
            self.x += 2
        elif self.bullet_direction == 4:
            self.x -= 2

        #Обновление позиции прямоугольника
        self.rect.y = self.y
        self.rect.x = self.x

    def draw_bullet(self):
        """Вывод снарядя на экран"""
        pygame.draw.rect(self.screen, self.color, self.rect)
