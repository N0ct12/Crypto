import math
import time
from collections import defaultdict


def calculate_entropy(frequency, total_bytes):
    entropy = -sum((freq / total_bytes) * math.log2(freq / total_bytes) for freq in frequency.values())
    return entropy


def calculate_byte_frequencies(data):
    frequency = defaultdict(int)
    for byte in data:
        frequency[byte] += 1
    return frequency


def extract_possible_keys(dump_data, key_length, entropy_threshold):
    key_candidates = {}
    total_bytes = key_length

    window = dump_data[:key_length]
    frequency = calculate_byte_frequencies(window)
    entropy = calculate_entropy(frequency, total_bytes)

    if entropy >= entropy_threshold:
        candidate_bytes = bytes(window)
        key_candidates[candidate_bytes] = key_candidates.get(candidate_bytes, 0) + 1

    for i in range(1, len(dump_data) - key_length + 1):
        old_byte = dump_data[i - 1]
        new_byte = dump_data[i + key_length - 1]

        frequency[old_byte] -= 1
        if frequency[old_byte] == 0:
            del frequency[old_byte]
        frequency[new_byte] += 1

        entropy = calculate_entropy(frequency, total_bytes)
        if entropy >= entropy_threshold:
            candidate_bytes = bytes(dump_data[i:i + key_length])
            key_candidates[candidate_bytes] = key_candidates.get(candidate_bytes, 0) + 1

    return [key for key, count in key_candidates.items() if count >= 2]


def find_keys(dump_file, entropy_threshold, key_length=16):
    start_time = time.time()
    with open(dump_file, 'rb') as file:
        dump_data = file.read()
    keys = extract_possible_keys(dump_data, key_length, entropy_threshold)
    return keys, time.time() - start_time


dump_file = 'source/dump_003.DMP'
entropy_threshold = 3
keys, full_time = find_keys(dump_file, entropy_threshold=entropy_threshold)
print(f"Всего ключей выбрано: {len(keys)}")
print(f'Время поиска ключей: {full_time:.2f} секунд')
