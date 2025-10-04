"""Simple ingest: PDF -> images using pdf2image
"""
from pathlib import Path
from typing import List
from pdf2image import convert_from_path


def pdf_to_images(pdf_path: str, out_dir: str, dpi: int = 200) -> List[str]:
    """Convert a PDF into JPEG images, one per page.

    Returns list of file paths written.
    """
    pdf = Path(pdf_path)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    pages = convert_from_path(str(pdf), dpi=dpi)
    out_files = []
    for i, page in enumerate(pages, start=1):
        out_path = out / f"{pdf.stem}_page_{i:03}.jpg"
        page.save(out_path, "JPEG")
        out_files.append(str(out_path))
    return out_files


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python ingest.py input.pdf output_dir")
        raise SystemExit(1)
    print(pdf_to_images(sys.argv[1], sys.argv[2]))
