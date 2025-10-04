# services/api/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
from pipelines.run_pipeline import process_pdf

app = FastAPI(title="Automated Dataset API")

# Directories
BASE = Path(__file__).resolve().parents[2]  # Project root
UPLOAD_DIR = BASE / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ANNOTATIONS_DIR = BASE / "data" / "annotations"
ANNOTATIONS_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return JSONResponse(status_code=400, content={"error": "File must be a PDF"})

    pdf_path = UPLOAD_DIR / file.filename

    # Save uploaded PDF
    with open(pdf_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Process PDF with full pipeline
    dataset = process_pdf(pdf_path)

    return {"message": "PDF processed successfully", "dataset": dataset, "path": str(pdf_path)}


@app.get("/list_uploads")
async def list_uploads():
    pdf_files = sorted([f.name for f in UPLOAD_DIR.glob("*.pdf")])
    return {"uploads": pdf_files}
