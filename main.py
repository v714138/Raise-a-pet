import os
import pygame

pygame.init()
size = 700, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Raise a Pet!')

all_sprites = pygame.sprite.Group()
button_sprites = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Button(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__(all_sprites)
        self.original_image = load_image(image_path, color_key=-1)
        self.image = pygame.transform.scale(self.original_image, (70, 70))
        self.rect = self.image.get_rect(topleft=position)

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class BarsikSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Indicator:
    def __init__(self, name, position, max_value):
        self.name = name
        self.position = position
        self.max_value = max_value
        self.current_value = max_value

    def update(self, value):
        self.current_value = max(0, min(self.max_value, value))

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), (*self.position, 200, 20))
        fill_width = (self.current_value / self.max_value) * 200
        pygame.draw.rect(surface, (0, 255, 0), (*self.position, fill_width, 20))
        font = pygame.font.Font(None, 24)
        text = font.render(f"{self.name}: {self.current_value}/{self.max_value}", True, (0, 0, 0))
        surface.blit(text, (self.position[0] + 5, self.position[1] - 25))


def main():
    hunger_indicator = Indicator("Голод", (50, 50), 100)
    health_indicator = Indicator("Здоровье", (50, 100), 100)
    sleep_indicator = Indicator("Сон", (50, 150), 100)
    fun_indicator = Indicator("Веселье", (50, 200), 100)

    barsik = BarsikSprite(load_image("Barsik.jpg"), 4, 8, 160, 160)
    food = Button('food.png', (0, 0))
    aidkit = Button('Aidkit.png', (100, 0))
    button_sprites.add(food)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    clicked_buttons = [button for button in button_sprites if button.rect.collidepoint(mouse_pos)]
                    if clicked_buttons:
                        print("Button clicked!")

        hunger_indicator.update(hunger_indicator.current_value - 0.1)
        health_indicator.update(health_indicator.current_value)
        sleep_indicator.update(sleep_indicator.current_value - 0.05)
        fun_indicator.update(fun_indicator.current_value + 0.1)

        all_sprites.update()
        screen.fill(pygame.Color("white"))
        hunger_indicator.draw(screen)
        health_indicator.draw(screen)
        sleep_indicator.draw(screen)
        fun_indicator.draw(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(2)

    pygame.quit()


if __name__ == '__main__':
    main()
