import pygame
import os

scale_factor = 1
MOVE_SPEED = 7
WIDTH = 110
HEIGHT = 90

COLOR = "white"
JUMP_POWER = 10
GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз
ANIMATION_DELAY = 100  # скорость смены кадров в миллисекундах
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами


def load_and_scale_image(image_path, scale_factor):
    image = pygame.image.load(image_path)
    image.set_colorkey(image.get_at((0, 0)))
    scaled_image = pygame.transform.scale(image, (
        int(image.get_width() * scale_factor), int(image.get_height() * scale_factor)))

    return scaled_image


ANIMATION_LEFT = [
    load_and_scale_image(f"{ICON_DIR}/cat/part_3_0.png", scale_factor),
    load_and_scale_image(f"{ICON_DIR}/cat/part_3_1.png", scale_factor),
    load_and_scale_image(f"{ICON_DIR}/cat/part_3_2.png", scale_factor),
    load_and_scale_image(f"{ICON_DIR}/cat/part_3_3.png", scale_factor),
]
ANIMATION_JUMP_LEFT = [load_and_scale_image(f"{ICON_DIR}/cat/part_3_0.png", scale_factor), ]
ANIMATION_JUMP_RIGHT = [load_and_scale_image(f"{ICON_DIR}/cat/part_1_3.png", scale_factor), ]
ANIMATION_JUMP = [load_and_scale_image(f"{ICON_DIR}/cat/part_0_3.png", scale_factor)]
ANIMATION_STAY = [load_and_scale_image(f"{ICON_DIR}/cat/part_0_2.png", scale_factor)]
ANIMATION_RIGHT = [
    load_and_scale_image(f"{ICON_DIR}/cat/part_1_0.png", scale_factor),
    load_and_scale_image(f"{ICON_DIR}/cat/part_1_1.png", scale_factor),
    load_and_scale_image(f"{ICON_DIR}/cat/part_1_2.png", scale_factor),
    load_and_scale_image(f"{ICON_DIR}/cat/part_1_3.png", scale_factor),
]


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.yvel = 0
        self.onGround = False
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill(pygame.Color(COLOR))
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)
        self.image.set_colorkey(pygame.Color(COLOR))

        # Инициализация анимаций
        self.animations = {
            'right': ANIMATION_RIGHT,
            'left': ANIMATION_LEFT,
            'jump_left': ANIMATION_JUMP_LEFT,
            'jump_right': ANIMATION_JUMP_RIGHT,
            'stay': ANIMATION_STAY,
        }
        self.current_animation = 'stay'
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()

    def update(self, left, right, up, platforms):
        # В зависимости от направления героя, выберается группа и фрейм анимации
        now = pygame.time.get_ticks()
        if now - self.last_update > ANIMATION_DELAY:
            self.last_update = now
            if self.current_animation in self.animations:
                frames = self.animations[self.current_animation]
                if frames:  # Проверяем, что список не пуст
                    self.current_frame = (self.current_frame + 1) % len(frames)

        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER
            self.current_animation = 'jump_right' if right else 'jump_left'
            self.current_frame = 0  # Сброс кадра при прыжке

        if left:
            self.xvel = -MOVE_SPEED
            self.current_animation = 'left'
        elif right:
            self.xvel = MOVE_SPEED
            self.current_animation = 'right'
        else:
            self.xvel = 0
            if not up:
                self.current_animation = 'stay'

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

        # Обновление изображения
        if self.current_animation in self.animations:
            frames = self.animations[self.current_animation]
            if frames:  # Проверяем, что список не пуст
                # Проверяем, что current_frame не выходит за пределы
                if self.current_frame < len(frames):
                    self.image = frames[self.current_frame]
                else:
                    self.current_frame = 0  # Сброс на 0, если индекс выходит за пределы

    def collide(self, xvel, yvel, platforms):
         # Проверка столкновения с другими спрайтами
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:  # Движение вправо
                    self.rect.right = p.rect.left
                if xvel < 0:  # Движение влево
                    self.rect.left = p.rect.right
                if yvel > 0:  # Движение вниз
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:  # Движение вверх
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
