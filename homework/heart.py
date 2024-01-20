import pygame
from pygame.sprite import Sprite

class Heart(Sprite):
    """Картинка сердца"""
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        self.image = pygame.image.load('image/hp_2.png')
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom