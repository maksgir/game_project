import pygame
import os
import sys
import random
import datetime as dt


class Enemy:
    def __init__(self, speed):
        self.r = random.randint(10, 790)
        self.x = self.r
        self.y = 0
        self.speed = speed

    def render(self, screen):
        pygame.draw.circle(screen, 'black', (self.x, self.y), 5)

    def move(self):
        self.y += self.speed


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
    enemy = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy, 10)
    clock = pygame.time.Clock()
    speed = 2
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
                print('Игра началась')
                game_started = True
                game_timer = Timer(dt.datetime.now())
                print(dt.datetime.now())
            if event.type == enemy and game_started:
                screen.fill((100, 149, 237))
                for en in enemies:
                    en.move()
                    pygame.draw.circle(screen, 'black', (en.x, en.y), 15)

        if game_timer != None:
            if game_timer.run():
                print('Создаю врага')
                a = Enemy(speed)
                enemies.append(a)
                print(len(enemies))
        for en in enemies:
            if en.y >= height + 20:
                enemies.remove(en)

        pygame.display.flip()

    pygame.quit()
