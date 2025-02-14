import sys

import pygame
from pygame import *

from sprites.game import Door, Coin, camera_configure, Camera, Platform, PLATFORM_WIDTH, PLATFORM_HEIGHT
from sprites.player import Player


WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#9d948b"


def play_screen():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(Color(BACKGROUND_COLOR))

    hero = Player(55, 700)
    left = right = False
    up = False

    coins = pygame.sprite.Group()

    total_coins_collected = 0
    entities = pygame.sprite.Group()
    platforms = []

    entities.add(hero)

    with open('data/level.txt') as file:
        level = file.readlines()

    timer = pygame.time.Clock()
    # Отрисовка уровня
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            elif col == "c":
                coin = Coin(x, y)
                entities.add(coin)
                coins.add(coin)
            elif col == "d":
                door = Door(x, y)
                entities.add(door)

            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0
    # Вычисление ширины и высоты всего уровня
    total_level_width = len(level[0]) * PLATFORM_WIDTH
    total_level_height = len(level) * PLATFORM_HEIGHT

    camera = Camera(camera_configure, total_level_width, total_level_height)
    # Основной цикл игры
    while True:
        timer.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_UP:
                up = True
            if event.type == KEYDOWN and event.key == K_LEFT:
                left = True
            if event.type == KEYDOWN and event.key == K_RIGHT:
                right = True

            if event.type == KEYUP and event.key == K_UP:
                up = False
            if event.type == KEYUP and event.key == K_RIGHT:
                right = False
            if event.type == KEYUP and event.key == K_LEFT:
                left = False

        screen.blit(bg, (0, 0))

        camera.update(hero)
        hero.update(left, right, up, platforms)
        # Столкновение игрока и монетки
        collected_coins = pygame.sprite.spritecollide(hero, coins, True)
        if collected_coins:
            total_coins_collected += len(collected_coins)
        # Столкновение с дверкой
        if pygame.sprite.collide_rect(hero, door):
            return total_coins_collected
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()
