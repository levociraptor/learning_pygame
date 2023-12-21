import pygame

class Ship():
    """Класс для управлением кораблем"""

    def __init__(self, ai_game):
        """Инициазлирует корабль и задает его начальную позицию"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        #загружаем изображение корабля и получаем прямоугольник
        self.image = pygame.image.load('image/ship.bmp')
        self.rect = self.image.get_rect()

        #каждый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom

        #сохранение вещественной координаты центра корабля
        self.x = float(self.rect.x)

        #Флаги перемещения
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Обновляет позиуию корабля с учетом флагов"""
        #Обноляется атрибут x, не rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        #Обновление атрибута rect на основании self.x.
        self.rect.x = self.x

    def blitme(self):
        '''Рисует корабль в текущей позиции'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Размещает корабль в центре нижней стороны"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
