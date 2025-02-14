from datetime import datetime

import pygame

from gameover import gameover
from loading import loading
from level import play_screen
from sprites.barsik import BarsikSprite
from sprites.button import Button
from sprites.coin import Coin
from sprites.indicator import Indicator
from utils import load_image

# Параметры экрана
pygame.init()
size = 800, 640
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Raise a Pet!')
background_image = load_image("fon_.jpg")
background_image.set_alpha(128)

# Группы спрайтов
all_sprites = pygame.sprite.Group()
button_sprites = pygame.sprite.Group()

# Отображение количества монет
def draw_coins(coins, screen):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(f"Монетки: {coins}", True, (0, 0, 0))
    screen.blit(text_surface, (620, 30))

# Главная функция игры
def main():
    #Индикаторы
    hunger_indicator = Indicator("Голод", (590, 100), 100)
    health_indicator = Indicator("Здоровье", (590, 150), 100)
    fun_indicator = Indicator("Веселье", (590, 200), 100)

    total_coins = 10
    start_time = datetime.now()
    barsik = BarsikSprite(
        sheet=load_image("Barsik.png"),
        columns=4, rows=8,
        frame_indices=[0, 0, 1, 1, 2, 2, 3, 3, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 23],
        scale_factor=1.5,
        x=250,
        y=250
    )
    # Кнопки
    food = Button('food_old.png', (0, 0), 'food')
    aidkit = Button('Aidkit.png', (100, 0), 'aidkit')
    play = Button('play.png', (200, 0), 'play')
    coin = Coin('Coin.png', (590, 30), 'coin')
    button_sprites.add(food)
    button_sprites.add(aidkit)
    button_sprites.add(play)
    all_sprites.add(barsik)
    all_sprites.add(aidkit)
    all_sprites.add(food)
    all_sprites.add(play)
    all_sprites.add(coin)

    clock = pygame.time.Clock()

    # Заставка
    loading(screen, *size)
    running = True
    # Основной цикл игры
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    clicked_buttons = [button for button in button_sprites if button.rect.collidepoint(mouse_pos)]
                    if clicked_buttons:
                        if clicked_buttons[0].type == 'food':
                            if total_coins > 0:
                                total_coins -= 1
                                hunger_indicator.regeneration()
                        elif clicked_buttons[0].type == 'aidkit':
                            if total_coins > 0:
                                total_coins -= 1
                                health_indicator.regeneration()
                        elif clicked_buttons[0].type == 'play':
                            coins = play_screen()
                            total_coins += coins
                            fun_indicator.regeneration()

        # Обновление индикаторов
        hunger_indicator.update(hunger_indicator.current_value - 2)
        health_indicator.update(health_indicator.current_value - 1)
        fun_indicator.update(fun_indicator.current_value - 3)
        if all(indicator.get_current_value() <= 0 for indicator in [hunger_indicator, health_indicator, fun_indicator]):
            duration = datetime.now() - start_time
            gameover(screen, *size, duration)

        all_sprites.update()
        # Отрисовка спрайтов
        screen.fill(pygame.Color("grey"))
        screen.blit(background_image, (0, 0))
        hunger_indicator.draw(screen)
        health_indicator.draw(screen)
        fun_indicator.draw(screen)
        all_sprites.draw(screen)
        draw_coins(total_coins, screen)
        pygame.display.flip()
        clock.tick(2)

    pygame.quit()


if __name__ == '__main__':
    main()
