# pipelines/ocr.py
from typing import List
from PIL import Image
import pytesseract

def ocr_images(image_paths: List[str]) -> List[str]:
    """Run OCR on a list of images and return extracted texts."""
    texts = []
    for img_path in image_paths:
        try:
            img = Image.open(img_path)
            text = pytesseract.image_to_string(img)
            texts.append(text)
        except Exception as e:
            print(f"Error reading {img_path}: {e}")
            texts.append("")
    return texts
