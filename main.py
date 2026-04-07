from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from cryptography.fernet import Fernet
import os
import io

app = FastAPI()

# Encryption key
KEY_FILE = "secret.key"

if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
else:
    with open(KEY_FILE, "rb") as f:
        key = f.read()

cipher = Fernet(key)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    raw = await file.read()
    encrypted = cipher.encrypt(raw)

    save_path = os.path.join(UPLOAD_DIR, file.filename + ".enc")
    with open(save_path, "wb") as f:
        f.write(encrypted)

    return {"status": "success", "file": file.filename}

@app.get("/download/{filename}")
def download_file(filename: str):
    path = os.path.join(UPLOAD_DIR, filename + ".enc")

    if not os.path.exists(path):
        return {"error": "File not found"}

    with open(path, "rb") as f:
        encrypted = f.read()

    decrypted = cipher.decrypt(encrypted)

    return StreamingResponse(
        io.BytesIO(decrypted),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )