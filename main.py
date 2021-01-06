import pygame
import os
import sys
import random
import datetime as dt

width, height = 800, 800


class HomeTown:
    def __init__(self):
        self.health = 1000
        self.x = 0
        self.y = 770
        self.max_health = 1000

    def render(self, screen):
        x = self.x
        y = self.y
        len_x = 800
        len_y = 8
        pygame.draw.rect(screen, (255, 255, 255), ((x, y), (len_x, len_y)))
        new_x = self.health / self.max_health * len_x
        if self.health > 0:
            pygame.draw.rect(screen, (0, 255, 0), ((x, y), (new_x, len_y)))


class Patron:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = 20

    def move(self):
        self.y -= self.speed

    def render_shot(self):
        pygame.draw.circle(screen, 'red', (self.x, self.y), 5)
        self.move()


class Enemy:
    def __init__(self, speed):
        self.r = random.randint(30, width - 30)
        self.x = self.r
        self.y = 0
        self.speed = speed
        self.max_health = 100
        self.health = 100
        self.damage = 250

    def render(self, screen):
        pygame.draw.circle(screen, (128, 0, 128), (self.x, self.y), 25)
        len_x = 100
        len_y = 10
        x = self.x - len_x // 2
        y = self.y - 50
        pygame.draw.rect(screen, (0, 0, 0), ((x, y), (len_x, len_y)), 2)
        pygame.draw.rect(screen, (255, 255, 255), ((x, y), (len_x, len_y)))
        new_x = self.health / self.max_health * len_x
        pygame.draw.rect(screen, (0, 255, 0), ((x, y), (new_x, len_y)))

    def move(self):
        self.y += self.speed


class Hero:
    def __init__(self, speed):
        self.x = width // 2
        self.y = height - 50
        self.speed = speed

    def render(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), ((self.x - 40, self.y), (80, 18)))
        pygame.draw.rect(screen, (128, 0, 0), ((self.x - 5, self.y - 10), (10, 10)))

    def move_left(self):
        if self.x - 40 > 0:
            self.x -= self.speed

    def move_right(self):
        if self.x + 40 < 800:
            self.x += self.speed


class Timer:
    def __init__(self, time, gap):
        self.timing = time
        self.gap = gap
        self.interval = dt.timedelta(seconds=self.gap)

    def run(self):
        now = dt.datetime.now()
        if now >= self.timing + self.interval:
            self.timing = dt.datetime.now()
            return True
        return False


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Игра')
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)

    enemies = []
    patrons = []

    enemy = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy, 10)
    clock = pygame.time.Clock()
    hero = pygame.USEREVENT + 1
    pygame.time.set_timer(hero, 10)

    running = True
    enemy_is_spoted = False
    game_started = False
    game_timer = None
    player_shot = False
    player = None
    home = None
    game_ended = False

    speed_of_enemy = 0.5
    speed_of_player = 3
    speed_of_patron = 5
    kills = 0
    enemy_spot_speed = 3.5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
                print('Игра началась')
                game_started = True
                game_timer = Timer(dt.datetime.now(), enemy_spot_speed)
                player = Hero(speed_of_player)
                home = HomeTown()

            if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]:
                player.move_left()

            if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
                player.move_right()
            if event.type == pygame.MOUSEBUTTONDOWN and game_started:
                player_shot = True
                p = Patron(player.x, player.y, speed_of_patron)
                patrons.append(p)
            if event.type == enemy and game_started:
                screen.fill((0, 0, 0))

                for en in enemies:
                    en.move()

                    if en.y >= 770:
                        home.health -= en.damage
                        enemies.remove(en)

                    en.render(screen)

                    if home.health <= 0:
                        print('Вы проиграли')
                        game_ended = True
                        game_started = False

            if event.type == hero and game_started:
                if player_shot:
                    for p in patrons:
                        p.render_shot()
                        if p.y <= - 20:
                            patrons.remove(p)

                        for e in enemies:
                            if e.y - 25 <= p.y - 5 <= e.y + 25 and e.x - 25 <= p.x + 5 <= e.x + 25:

                                e.health -= p.damage

                                patrons.remove(p)
                                if e.health <= 0:
                                    # print('Убит')
                                    kills += 1
                                    enemies.remove(e)
                                    if kills % 5 == 0:
                                        enemy_spot_speed -= 0.5
                                        speed_of_enemy += 0.5
                                        game_timer = Timer(dt.datetime.now(), enemy_spot_speed)
                                        print('Уровень пройден')
                                    print(kills)
                home.render(screen)
                player.render(screen)
        if game_timer != None and game_started:
            if game_timer.run():
                # print('Создаю врага')
                a = Enemy(speed_of_enemy)
                enemies.append(a)

        for en in enemies:
            if en.y >= height + 20:
                enemies.remove(en)

        pygame.display.flip()
        if game_ended:
            patrons = []
            enemies = []
            game_ended = False
            speed_of_enemy = 0.5
            speed_of_player = 3
            speed_of_patron = 5
            kills = 0
            enemy_spot_speed = 3.5

    pygame.quit()
