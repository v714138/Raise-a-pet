import pygame

class BarsikSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows,  x, y, scale_factor=1,frame_indices=None):
        super().__init__()
        self.frames = []
        self.load_frames(sheet, columns, rows, frame_indices, scale_factor)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect(topleft=(x, y))

    def load_frames(self, sheet, columns, rows, frame_indices, scale_factor):
        frame_width = sheet.get_width() // columns
        frame_height = sheet.get_height() // rows
        if frame_indices is None:
            frame_indices = range(columns * rows)
        for index in frame_indices:
            row = index // columns
            col = index % columns
            frame_location = (col * frame_width, row * frame_height)
            frame = sheet.subsurface(pygame.Rect(frame_location, (frame_width, frame_height)))
            if scale_factor != 1.0:
                frame = pygame.transform.scale(frame,
                                               (int(frame_width * scale_factor), int(frame_height * scale_factor)))
            self.frames.append(frame)

    def update(self):
        if self.frames:  # Проверяем, есть ли кадры
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
