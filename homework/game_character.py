import pygame

class Game_char():
    """Клас для управления игровым персонажем"""

    def __init__(self, window):
        """Инициализирует кончателя  и задает его позицию"""
        self.screen = window.screen
        self.screen_rect = window.screen.get_rect()

        #Загружает изобраежение персонажа и получаем прямоугольник
        self.image = pygame.image.load('image/кончатель.png')
        self.rect = self.image.get_rect()

        #Задает позицию персонажу
        self.rect.midbottom = self.screen_rect.midbottom

        #Флаги перемещения
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        #Счетчик собранных звезд
        self.collected_stars = 0

        self.hit_points = 3

    def update(self, window):
        """функция отвечает за перемещение персонажа"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += 1.5
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= 1.5
        if self.moving_up and self.rect.top > 0:
            self.rect.y -= 1.5
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += 1.5

    def center_char(self):
        """Перемещает персонажа в изначальное положение"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)


    def blitme(self):
        """Рисует кончателя в заданой позиции"""
        self.screen.blit(self.image, self.rect)

