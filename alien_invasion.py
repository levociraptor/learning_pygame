import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class Alien_invasion:
    """Класс для управленя ресурсами и поведением игры"""

    def __init__(self):
        """Инициализируют игры и создает игоровые ресурсы"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Создание экземпляра для хранения игровой статистики
        # И панели инструментов
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #Создание кноки Play
        self.play_button = Button(self, "Play")

        #Создание кнопок сложности
        self.easy_button = Button(self, "Easy", -500)
        self.medium_button = Button(self, "Medium", 0 )
        self.hard_button = Button(self, "Hard", 500)
        self.difficulty_selection = True


    def run_game(self):
        """Запуск основого цикла игры"""
        while True:
            self._check_events()
            if self.stats.game_active and not self.difficulty_selection:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("record.txt", "w") as rec:
                    rec.write(str(self.stats.high_score))
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.play_button.rect.collidepoint(mouse_pos):
                    self._check_play_button()
                if self.medium_button.rect.collidepoint(mouse_pos):
                    self._check_medium_difficulty_button()
                elif self.easy_button.rect.collidepoint(mouse_pos):
                    self.difficulty_selection = False
                    pygame.mouse.set_visible(False)
                elif self.hard_button.rect.collidepoint(mouse_pos):
                    self._check_hard_difficulty_button()

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            with open("record.txt", "w") as rec:
                rec.write(str(self.stats.high_score))
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._check_play_button()

    def _check_keyup_events(self, event):
        """Реаигирует на отпускание клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self):
        """Запускает новую игру при нажатии кнопки Play"""
        if not self.stats.game_active and not self.difficulty_selection:
            # Сброс игровых настроек
            self.settings.initialize_dynamic_settings()

            # Cброс игровой статистики
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_images()

            # Отчистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            # Указатель мыши скрывается
            pygame.mouse.set_visible(False)

    def _check_medium_difficulty_button(self):
        "Увеличивает скорость инопланетян до 1"
        if self.difficulty_selection:
            self.settings.alien_speed_factor = 0.5
            self.difficulty_selection = False
            pygame.mouse.set_visible(False)

    def _check_hard_difficulty_button(self):
        "Увеличивает скорость инопланетян до 1.5"
        if self.difficulty_selection:
            self.settings.alien_speed_factor = 0.75
            self.difficulty_selection = False
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в шруппу bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды"""
        #Обновление позиции снаряда
        self.bullets.update()

        #Удаление снарядов, за пределами экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Обработка коллизий снарядов с пришельцами"""
        # Удаление снарядов и пришельцев участвующих в колизиях
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self._start_new_level()

    def _start_new_level(self):
        """Удаляет снаряды, создает новый флот и увеличивает уровень"""
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        # Увелечение уровня
        self.stats.level += 1
        self.sb.prep_level()


    def _update_aliens(self):
        """Обновляет позиции пришельцев"""
        self._check_fleet_edges()
        self.aliens.update()

        # Проверка коллизий "пришелец - корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #Проверить, добрались ли пришельцы до нижнего края экрана
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Создание флота пришельцев"""
        #Создание пришельца и вычисление количества пришельцев в ряду
        #Интервал между соседними пришельцами равен ширине пришельца
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #Определяет количество рядов, помещающихся на экране
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #Создание перрвого ряда пришельцев
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем"""
        if self.stats.ship_left > 0:
            #Уменьшение ship_left и обновление панели счета
            self.stats.ship_left -= 1
            self.sb.prep_ships()

            #Очистка списков пришельца и снарядов
            self.aliens.empty()
            self.bullets.empty()

            #Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            #Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Происходит то же, что при столкновении с кораблем
                self._ship_hit()
                break

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран"""
        self.screen.fill(self.settings.bg_color )
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet( )
        self.aliens.draw(self.screen)

        # Вывод информации о счете
        self.sb.show_score()

        #Кнопка Play отображается в том члучае, если игра неактивна
        if not self.stats.game_active and not self.difficulty_selection:
            self.play_button.draw_button()

        if self.difficulty_selection:
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()


        pygame.display.flip()


if __name__ == '__main__':
    #Создание экземпляра и запуск игры.
    ai = Alien_invasion()
    ai.run_game()
