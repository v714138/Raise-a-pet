import pygame


class Indicator:
    def __init__(self, name, position, max_value):
        self.name = name
        self.position = position
        self.max_value = max_value
        self.current_value = max_value

    def get_current_value(self):
        return self.current_value

    def update(self, value):
        self.current_value = max(0, min(self.max_value, value))

    def regeneration(self):
        self.current_value = self.max_value

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), (*self.position, 200, 20))
        fill_width = (self.current_value / self.max_value) * 200
        pygame.draw.rect(surface, (0, 255, 0), (*self.position, fill_width, 20))
        font = pygame.font.Font(None, 24)
        text = font.render(f"{self.name}: {self.current_value}/{self.max_value}", True, (0, 0, 0))
        surface.blit(text, (self.position[0] + 5, self.position[1] - 25))
