import pygame
from pygame import *
import os

PLATFORM_WIDTH = 55
PLATFORM_HEIGHT = 45
PLATFORM_COLOR = "#FF6262"
ICON_DIR = os.path.dirname(__file__)

WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640  # Высота

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    target_left, target_top, _, _ = target_rect
    camera_left, camera_top, camera_width, camera_height = camera

    # Вычисляем новые координаты камеры
    camera_left = -target_left + WIN_WIDTH / 2
    camera_top = -target_top + WIN_HEIGHT / 2

    # Ограничиваем движение камеры
    camera_left = min(0, camera_left)  # Не движемся дальше левой границы
    camera_left = max(-(camera.width - WIN_WIDTH), camera_left)  # Не движемся дальше правой границы
    camera_top = max(-(camera.height - WIN_HEIGHT), camera_top)  # Не движемся дальше нижней границы
    camera_top = min(0, camera_top)  # Не движемся дальше верхней границы

    return Rect(camera_left, camera_top, camera_width, camera_height)

class Platform(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = image.load(os.path.join(ICON_DIR, "blocks/platform.png")).convert_alpha()
        self.image = transform.scale(self.image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = image.load(os.path.join(ICON_DIR, "data/Coin.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (55, 45))
        self.rect = self.image.get_rect(center=(x, y))

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((55, 45))  # Измените размер на 50x80
        self.image.fill((139, 69, 19))  # Цвет двери
        self.rect = self.image.get_rect(topleft=(x, y))
