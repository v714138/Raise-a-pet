import pygame

from utils import load_image

class Coin(pygame.sprite.Sprite):
    def __init__(self, image_path, position, type):
        super().__init__()
        self.original_image = load_image(image_path, color_key=-1)
        self.image = pygame.transform.scale(self.original_image, (20, 20))
        self.rect = self.image.get_rect(topleft=position)
        self.type = type

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)