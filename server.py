from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import os

from utils.file_ops import save_encrypted_file, load_decrypted_file

app = FastAPI()

# Allow Flutter, mobile, desktop, etc.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Upload (Encrypt + Save)
@app.post("/upload")
async def upload_file(file: UploadFile):
    try:
        raw_bytes = await file.read()
        save_encrypted_file(file.filename, raw_bytes)
        return {"message": "File uploaded & encrypted", "file": file.filename}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------
# Download (Decrypt + Stream)
@app.get("/download/{filename}")
async def download_file(filename: str):
    try:
        decrypted_bytes = load_decrypted_file(filename)

        return StreamingResponse(
            iter([decrypted_bytes]),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------
# List Files
@app.get("/files")
async def list_files():
    folder = "storage/uploads"
    try:
        files = os.listdir(folder)
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))