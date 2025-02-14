import sys
import time

import pygame

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)


def loading(screen, width, height):
    # Фоновая заставка
    background_image = pygame.image.load('data/cat_load.jpg')
    background_image = pygame.transform.scale(background_image, (width, height))
    # Надпись
    font = pygame.font.Font(None, 74)
    text = font.render("Raise a Pet!", True, black)
    # Первый экран загрузки или второй
    show_splash = True

    pygame.mixer.music.load('data/fon.mp3')
    pygame.mixer.music.play(-1)

    # Второй экран загрузчика
    def show_loader():
        loading = True
        while loading:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.blit(background_image, (0, 0))
            loading_text = font.render("Loading...", True, black)
            text_rect = loading_text.get_rect(center=(width // 2, height // 2 - 50))
            screen.blit(loading_text, text_rect)

            pygame.draw.rect(screen, white, (width // 2 - 100, height // 2, 200, 30))
            pygame.draw.rect(screen, green, (width // 2 - 100, height // 2, 0, 30))

            for i in range(201):
                pygame.draw.rect(screen, green, (width // 2 - 100, height // 2, i, 30))
                pygame.display.flip()
                time.sleep(0.01)

            loading = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and show_splash:
                show_splash = False
                pygame.mixer.music.stop()

        if show_splash:
            screen.blit(background_image, (0, 0))
            text_rect = text.get_rect(center=(width // 2, height // 2))
            screen.blit(text, text_rect)
        else:
            show_loader()
            return

        pygame.display.flip()

    # Основной контент игры
    screen.blit(background_image, (0, 0))  # Отображаем фоновое изображение

    # Здесь можно добавить основной контент игры
    pygame.display.flip()

    # Основной цикл игры (после загрузки)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
