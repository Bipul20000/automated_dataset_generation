"""Minimal FastAPI app exposing endpoints for running pipeline steps (stubs).
"""
from fastapi import FastAPI, UploadFile, File
from pathlib import Path
import shutil

app = FastAPI(title="Automated Dataset API")

BASE = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BASE / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        return {"error": "only pdf files supported in this stub"}
    dest = UPLOAD_DIR / file.filename
    with open(dest, 'wb') as f:
        shutil.copyfileobj(file.file, f)
    return {"path": str(dest)}


@app.get("/list_uploads")
async def list_uploads():
    files = [str(p) for p in UPLOAD_DIR.iterdir() if p.is_file()]
    return {"uploads": files}
