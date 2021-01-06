import pygame
import os
import sys
import random
import datetime as dt

width, height = 800, 800


class Patron:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

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

    def render(self, screen):
        pygame.draw.circle(screen, (47, 79, 79), (self.x, self.y), 25)

    def move(self):
        self.y += self.speed


class Hero:
    def __init__(self, speed):
        self.x = width // 2
        self.y = height - 50
        self.speed = speed

    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 205), ((self.x - 60, self.y), (120, 18)))
        pygame.draw.rect(screen, (0, 0, 0), ((self.x - 5, self.y - 10), (10, 10)))

    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed


class Timer:
    def __init__(self, time):
        self.timing = time
        self.interval = dt.timedelta(seconds=1)

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
    running = True
    enemy_is_spoted = False
    game_started = False
    game_timer = None
    enemies = []
    patrons = []
    enemy = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy, 10)
    clock = pygame.time.Clock()
    hero = pygame.USEREVENT + 1
    pygame.time.set_timer(hero, 10)
    speed_of_enemy = 1
    speed_of_player = 3
    speed_of_patron = 5
    player_shot = False
    player = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
                print('Игра началась')
                game_started = True
                game_timer = Timer(dt.datetime.now())
                player = Hero(speed_of_player)
            if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]:
                player.move_left()

            if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
                player.move_right()
            if event.type == pygame.MOUSEBUTTONDOWN and game_started:
                player_shot = True
                p = Patron(player.x, player.y, speed_of_patron)
                patrons.append(p)
            if event.type == enemy and game_started:
                screen.fill((100, 149, 237))
                for en in enemies:
                    en.move()
                    en.render(screen)
            if event.type == hero and game_started:
                if player_shot:
                    for p in patrons:
                        p.render_shot()
                        if p.y <= - 20:
                            patrons.remove(p)
                        for e in enemies:
                            if e.y - 25 <= p.y - 5 <= e.y + 25 and e.x - 25 <= p.x + 5 <= e.x + 25:
                                enemies.remove(e)
                                patrons.remove(p)
                player.render(screen)
        if game_timer != None:
            if game_timer.run():
                print('Создаю врага')
                a = Enemy(speed_of_enemy)
                enemies.append(a)
                print(len(enemies))
        for en in enemies:
            if en.y >= height + 20:
                enemies.remove(en)

        pygame.display.flip()

    pygame.quit()
