import os
from utils.encryption import encrypt_bytes, decrypt_bytes
from config import AES_KEY

STORAGE_FOLDER = "storage/uploads"
IV_FOLDER = "storage/temp"

os.makedirs(STORAGE_FOLDER, exist_ok=True)
os.makedirs(IV_FOLDER, exist_ok=True)

# Save encrypted file + IV
def save_encrypted_file(filename: str, raw_bytes: bytes):
    iv, encrypted = encrypt_bytes(AES_KEY, raw_bytes)

    # Save encrypted file
    encrypted_path = os.path.join(STORAGE_FOLDER, filename)
    with open(encrypted_path, "wb") as f:
        f.write(encrypted)

    # Save IV separately
    iv_path = os.path.join(IV_FOLDER, filename + ".iv")
    with open(iv_path, "wb") as f:
        f.write(iv)

    return encrypted_path

# Load + decrypt file
def load_decrypted_file(filename: str) -> bytes:
    encrypted_path = os.path.join(STORAGE_FOLDER, filename)
    iv_path = os.path.join(IV_FOLDER, filename + ".iv")

    if not os.path.exists(encrypted_path):
        raise FileNotFoundError("Encrypted file not found")

    if not os.path.exists(iv_path):
        raise FileNotFoundError("IV file missing")

    with open(encrypted_path, "rb") as f:
        encrypted_bytes = f.read()

    with open(iv_path, "rb") as f:
        iv = f.read()

    return decrypt_bytes(AES_KEY, iv, encrypted_bytes)