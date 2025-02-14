import os
from PIL import Image

def cut_image(image_path, square_size, output_folder):
    # Открываем изображение
    image = Image.open(image_path)
    img_width, img_height = image.size

    # Создаем папку, если она не существует
    os.makedirs(output_folder, exist_ok=True)

    cols = img_width // square_size
    rows = img_height // square_size

    # Разрезаем изображение
    for row in range(rows):
        for col in range(cols):
            left = col * square_size
            upper = row * square_size
            right = left + square_size
            lower = upper + square_size

            # Создаем область для вырезания
            box = (left, upper, right, lower)
            part = image.crop(box)
            part = part.crop((30, 65, part.width-20, part.height - 5))
            new_size = (int(part.width * 0.5), int(part.height * 0.5))
            # part = part.resize(new_size, Image.LANCZOS)
            # Сохраняем вырезанную часть
            part.save(f"{output_folder}/part_{row}_{col}.png")

# Пример использования
cut_image("Barsik.png", 160, "cat")


# Пример использования
# cut_image("Barsik.jpg", 4, 8, "cat")
