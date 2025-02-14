import sys
import time

import pygame

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)


def gameover(screen, width, height, duration):
    font = pygame.font.Font(None, 74)
    text = font.render("Игра окончена!", True, black)

    image = pygame.image.load('./data/deadbarsik.png')
    image = pygame.transform.scale(image, (width // 2, height // 4))

    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    font_desc = pygame.font.Font(None, 50)
    text_desc = font_desc.render(f"Ваш кот прожил: {hours} часов {minutes} минут {seconds} секунд!", True, black)

    pygame.mixer.music.load('data/fon.mp3')
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

        screen.fill(white)
        text_rect = text.get_rect(center=(width // 2, 100))
        screen.blit(text, text_rect)

        text_desc_rect = text_desc.get_rect(center=(width // 2, 150))
        screen.blit(text_desc, text_desc_rect)
        image_rect = image.get_rect(center=(width // 2, height // 2 + 50))
        screen.blit(image, image_rect)

        pygame.display.flip()
