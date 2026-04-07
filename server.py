from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Folder where encrypted files are stored
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -------------------------------
# Upload Endpoint
# -------------------------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save encrypted bytes exactly as Flutter sends them
    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"message": "File uploaded", "filename": file.filename}


# -------------------------------
# List Files Endpoint
# -------------------------------
@app.get("/files")
def list_files():
    return os.listdir(UPLOAD_FOLDER)


# -------------------------------
# Download Endpoint
# -------------------------------
@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        return {"error": "File not found"}

    # Send encrypted file back to Flutter
    return FileResponse(file_path, filename=filename)