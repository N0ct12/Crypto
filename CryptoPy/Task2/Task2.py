from PIL import Image
import time


def crc_table():
    table = []
    polynomial = 0x1D
    for i in range(256):
        crc = i
        for j in range(8):
            if crc & 0x80:
                crc = ((crc << 1) & 0xFF) ^ polynomial
            else:
                crc = (crc << 1) & 0xFF
        table.append(crc)
    return table


def get_crc(data, table):
    crc = 0xFF
    for byte in data:
        crc = table[crc ^ byte]
    return crc ^ 0xFF


def extract_hidden_message(image_path):
    start_time = time.time()
    try:
        img = Image.open(image_path)
        width, height = img.size
        print(f"Картинка успешно загружена: {image_path} ")
    except Exception as e:
        print(f"Ошибка загрузки изображения: {e}")
        return

    result = bytearray()

    table = crc_table()
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            pixels = b << 24 | g << 16 | r << 8 | 0x00
            byte_pixels = pixels.to_bytes(4, 'big')
            result.append(get_crc(byte_pixels, table))
    return result, time.time()-start_time


crc_values, total_time = extract_hidden_message('I1.png')
with open('I2.jpeg', 'wb') as f:
    f.write(crc_values)
print("Картинка сохранена как I2.jpeg")
print(f"Алгоритм занял: {total_time:.2f} секунд")
