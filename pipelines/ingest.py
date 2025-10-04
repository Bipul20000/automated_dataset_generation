# pipelines/ingest.py
from pathlib import Path
from typing import List
from pdf2image import convert_from_path

def ingest_pdfs(pdf_path: str, out_dir: str = "data/uploads") -> List[str]:
    """Convert PDF to images and return list of image paths."""
    pdf = Path(pdf_path)
    out = Path(out_dir) / pdf.stem
    out.mkdir(parents=True, exist_ok=True)

    pages = convert_from_path(str(pdf))
    out_files = []
    for i, page in enumerate(pages, start=1):
        img_path = out / f"{pdf.stem}_page_{i:03}.jpg"
        page.save(img_path, "JPEG")
        out_files.append(str(img_path))
    return out_files
