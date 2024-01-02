import sys
from time import sleep
import pygame
from random import randint
from game_character import Game_char
from bullet import Bullet
from star import Star
from drop import Drop
from pig import Pig

class Window:
    """Класс для управления окном вывода игры"""

    def __init__(self):
        """Инициализирует игровое окно"""
        pygame.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Blue Window")

        self.char = Game_char(self)
        self.bullets = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.drops = pygame.sprite.Group()
        self.pigs = pygame.sprite.Group()

        self.bullet_direction = 1

        self.pigs_stars = 0

        self._create_stars()

        self._create_drops()

        self._create_pigs()

        self.bg_color = (255, 255, 255)

    def run_window(self):
        "Основной цикл игры"

        while True:
            self._check_ivents()
            if self.char.collected_stars <= 50 and self.char.hit_points > 0:
                self.char.update(self)
                self._update_stars()
                self._update_bullets()
                self._update_drops()
                self._update_pigs()

            self._update_window()

    def _check_ivents(self):
        """Метод проверяющий события с клавиатуры"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Реагируте на нажатие клавиш"""
        if event.key == pygame.K_RIGHT:
            self.char.moving_right = True
            self.bullet_direction = 2
        elif event.key == pygame.K_LEFT:
            self.char.moving_left = True
            self.bullet_direction = 4
        elif event.key == pygame.K_UP:
            self.char.moving_up = True
            self.bullet_direction = 1
        elif event.key == pygame.K_DOWN:
            self.char.moving_down = True
            self.bullet_direction = 3
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Реагируте на отжатие клавиш"""
        if event.key == pygame.K_RIGHT:
            self.char.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.char.moving_left = False
        elif event.key == pygame.K_UP:
            self.char.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.char.moving_down = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets"""
        new_bullet = Bullet(self, self.bullet_direction)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды"""
        #Обновление позиции снаряда
        self.bullets.update()

        #Удаление снарядов, вышедших за края экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            elif bullet.rect.bottom >= self.screen_height:
                self.bullets.remove(bullet)
            elif bullet.rect.left <= 0:
                self.bullets.remove(bullet)
            elif bullet.rect.right >= self.screen_width:
                self.bullets.remove(bullet)

    def _update_stars(self):
        """Удалает звезды при столкновение
        и создает новые если они закончились на карте"""
        # Создает новые звезды, когда собраны все старые
        if not self.stars:
            self._create_stars()

        # цикл удаляет звезду в случае коллизии
        for star in self.stars:
            collisions = self.char.rect.colliderect(star.rect)
            if collisions:
                self.char.collected_stars += 1
                self.stars.remove(star)

    def _update_drops(self):
        """Перемещает капли дождя вниз и перемещает их в самый верх
        если они достигли дна"""
        for drop in self.drops.sprites():
            drop.rect.y += 1
            if drop.rect.bottom >= self.screen_height:
                drop.rect.y = 0

    def _update_pigs(self):
        """Двигает свиней в случайном направление
        и обрабатывает коллизии"""
        #Перемещает свиней в случайном направление
        for pig in self.pigs:
            if pig.rect.right > self.screen_width:
                pig.direction = 4
                pig.direction_changer()
            elif pig.rect.left < 0:
                pig.direction = 2
                pig.direction_changer()
            elif pig.rect.top < 0:
                pig.direction = 1
                pig.direction_changer()
            elif pig.rect.bottom > self.screen_height:
                pig.direction = 3
                pig.direction_changer()
            else:
                pig.direction_changer()

            if collisions := pygame.sprite.groupcollide(self.bullets, self.pigs, True, False):
                pig.hit_points -= 1
                if pig.hit_points == 0:
                    self.pigs.remove((pig))

        #Перемещает персонажа на исходное место
        #и создает новых свиней в случае столкновения
        if pygame.sprite.spritecollideany(self.char, self.pigs):
            self._char_hit()

    def _char_hit(self):
        """Обрабатывает столкновение свиньи и персонажа"""
        #Уменьшение здоровья у персонажа
        self.char.hit_points -= 1

        #Удаление всеx свиней с экрана
        self.pigs.empty()

        #Создает новых свиней и перемещает персонажа в центр
        self._create_pigs()
        self.char.center_char()

        #Пауза
        sleep(0.5)

    def _create_stars(self):
        """Создание звездочек :3"""
        star = Star(self)
        star_width = star.rect.width
        star_height = star.rect.height

        # количество доступных столбцов для звезд
        available_space_x = self.screen_width - (2 * star_width)
        number_stars_x = available_space_x // (star_width * 2)

        #количество доступных рядов для звезд
        available_space_y = self.screen_height - (2 * star_height)
        number_stars_y = available_space_y // ( star_height * 2)

        #цикл, который перебирает координты по y и x
        for row in range(number_stars_y):
            for star_number in range(number_stars_x):
                self._create_star(row, star_number)

    def _create_star(self, row, star_number):
        """Создает каждую конкретную звезду в конкретном месте"""
        star = Star(self)
        star_width = star.rect.width
        star_height = star.rect.height
        star.rect.x = (2 * star_width) * star_number
        star.rect.y = (2 * star_height) * row
        key = randint(1,3)
        if key == 2:
            self.stars.add(star)

    def _create_drops(self):
        """Создание капель дождя"""
        drop = Drop(self)
        drop_width = drop.rect.width
        drop_height = drop.rect.height

        #количество столбцов для капель
        available_space_x = self.screen_width - (2 * drop_width)
        number_drop_x = available_space_x // (drop_width * 2)

        #количество рядов для капель
        available_space_y = self.screen_height
        number_drop_y = available_space_y // (drop_height * 2)

        flag = 1
        for row in range(number_drop_y):
            for column in range(number_drop_x):
                if flag == 1:
                    break
                key = randint(1, 8)
                self._create_drop(column, row, key)
            flag *= -1

    def _create_drop(self, column, row=1, key=3):
        """Создает каждую конкретную каплю в конкретном месте"""
        drop = Drop(self)
        drop_width = drop.rect.width
        drop_height = drop.rect.height
        drop.rect.x = (2 * drop_width) * column
        drop.rect.y = (2 * drop_height) * row
        if key == 3:
            self.drops.add(drop)

    def _create_pigs(self):
        """Создание свиней"""
        number_of_pigs = 3
        for i in range(number_of_pigs):
            pig = Pig(self)
            pig_width = pig.rect.width
            pig_height = pig.rect.height
            x_coord = randint(pig_width, self.screen_width - 2 * pig_width)
            y_coord = randint(pig_height, self.screen_height - 2 * pig_height)
            pig.rect.x = x_coord
            pig.rect.y = y_coord
            self.pigs.add(pig)

    def _update_window(self):
        # Перерисовывает экарн при каждом проходе цикла
        self.screen.fill(self.bg_color)
        self.char.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        #Отрисовывает звезды
        self.stars.draw(self.screen)

        #Отрисовывает капли
        self.drops.draw(self.screen)

        # Отрисовывает свиней
        self.pigs.draw(self.screen)

        # Отображает последний прорисованный экран
        pygame.display.flip()

if __name__ == "__main__":
    window = Window()
    window.run_window()