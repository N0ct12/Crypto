from keys import keys
from Crypto.Cipher import AES
from PIL import Image
import io


def verify_png_format(data):
    try:
        with Image.open(io.BytesIO(data)) as img:
            return img.format == 'PNG'
    except IOError:
        return False


def decrypt_message(encrypted_file, keys):
    with open(encrypted_file, 'rb') as file:
        encrypted_data = file.read()
    for key in keys:
        if len(key) == 16:
            cipher = AES.new(key, AES.MODE_ECB)
            decrypted_data = cipher.decrypt(encrypted_data)
            if verify_png_format(decrypted_data):
                return key, decrypted_data
    return IOError


encrypted_file = 'source/encr_003'

key, decrypted_data = decrypt_message(encrypted_file, keys)

if key:
    print(f'Ключ найден: {key.hex()}')
    with open('pwd.txt', 'w') as f:
        f.write(key.hex())
    with open('I1.png', 'wb') as f:
        f.write(decrypted_data)
    print('Сообщение расшифровано и сохранено как I1.png')
else:
    print('Ключ не найден или сообщение не удалось расшифровать')
