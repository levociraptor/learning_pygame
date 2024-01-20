import pygame.font

class Button:
    def __init__(self, game, text):
        """Инициализирует атрибуты кнопки"""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        #Размеры и цвета кнопки
        self.width, self.height = 200, 50
        self.button_color = (63, 131, 126)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 56)

        #Создание и позиционирвание прямоугольника
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self._prep_text(text)


    def _prep_text(self, text):
        """Создает прямоугольник с текстом и выравнивает его по середине"""
        self.text_image = self.font.render(text, True,
                                           self.text_color, self.button_color)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.rect.center

    def draw_button(self):
        #Вывод кнопки на экран
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.text_image, self.text_image_rect)
