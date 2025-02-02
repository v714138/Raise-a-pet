import sys

import pygame

clock = pygame.time.Clock()
FPS = 50

def terminate():
    pygame.quit()
    sys.exit()

def play_screen(screen):
    screen.fill(pygame.Color("white"))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)