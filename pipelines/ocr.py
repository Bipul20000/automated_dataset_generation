"""OCR extraction wrapper using pytesseract
"""
from pathlib import Path
from typing import List
import pytesseract
from PIL import Image


def image_to_text(image_path: str) -> str:
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text


def batch_ocr(image_paths: List[str]) -> List[str]:
    texts = []
    for p in image_paths:
        texts.append(image_to_text(p))
    return texts


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ocr.py image1.jpg [image2.jpg ...]")
        raise SystemExit(1)
    print(batch_ocr(sys.argv[1:]))
