from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

# Pads data to be a multiple of 16 bytes (AES block size)
def pad(data: bytes) -> bytes:
    padding_length = 16 - (len(data) % 16)
    return data + bytes([padding_length]) * padding_length

# Removes padding after decryption
def unpad(data: bytes) -> bytes:
    padding_length = data[-1]
    return data[:-padding_length]

# Encrypts raw bytes using AES-256-CBC
def encrypt_bytes(key: bytes, data: bytes) -> tuple[bytes, bytes]:
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data))
    return iv, encrypted

# Decrypts AES-256-CBC encrypted bytes
def decrypt_bytes(key: bytes, iv: bytes, encrypted_data: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted_data)
    return unpad(decrypted)