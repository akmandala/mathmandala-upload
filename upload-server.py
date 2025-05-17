from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import os
from datetime import datetime
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/uploads")
def list_uploads():
    files = os.listdir(UPLOAD_DIR)
    return {"files": files}

@app.post("/upload")
async def upload(file: UploadFile = File(...), name: str = Form(...), subject: str = Form(...)):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"mathmandala_{name}_{subject}_{timestamp}.jpg"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return JSONResponse({"status": "ok", "filename": filename})

@app.delete("/delete/{filename}")
def delete_file(filename: str):
    filepath = os.path.join("/tmp/uploads", filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return {"status": "deleted", "filename": filename}
    else:
        raise HTTPException(status_code=404, detail="File not found")

