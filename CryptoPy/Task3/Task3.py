from Crypto.Cipher import AES
import hashlib
import time


def get_img_data(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    marker = b'\xFF\xD9'
    index = data.find(marker)
    if index == -1:
        raise ValueError("Не найден маркер")

    clean_part = data[:index + len(marker)]
    dirty_part = data[index + len(marker):]

    return clean_part, dirty_part


def get_md5(data):
    md5 = hashlib.md5()
    md5.update(data)
    return md5.digest()


def decrypt_aes_cbc(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(data)
    return decrypted_data


start_time = time.time()
try:
    clean_data, encrypted_data = get_img_data('I2.jpeg')
except ValueError as e:
    exit(e)

encrypted_part = encrypted_data[:16]

K1 = bytes.fromhex('022fe70a8753658e4d360ac459d83764')
K2 = get_md5(clean_data)

print(f"K2: {K2.hex()}")
print(f"IV (K1): {K1.hex()}")

try:
    decrypted_data = decrypt_aes_cbc(encrypted_part, K2, K1)
    try:
        password = decrypted_data.decode('ASCII')
        if all(32 <= ord(c) <= 126 for c in password):
            print("Пароль:", password)
            print(f"Время работы алгоритма: {time.time()-start_time:.4f} сек")
            with open('pwd.txt', 'w') as f:
                f.write(password)
    except UnicodeDecodeError:
        print("Ошибка расшифровки в ASCII")
except ValueError as e:
    print(f"Ошибка расшифровки: {e}")
