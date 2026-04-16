import os

# 32‑byte AES‑256 key

KEY_FILE = "aes_key.bin"

def load_key() -> bytes:
    if not os.path.exists(KEY_FILE):
        key = os.urandom(32)  # AES‑256 = 32 bytes
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key

    with open(KEY_FILE, "rb") as f:
        return f.read()

AES_KEY = load_key()