# pipelines/run_pipeline.py
from pathlib import Path
import json
from pipelines.ingest import ingest_pdfs
from pipelines.ocr import ocr_images
from pipelines.alignment import align_images_texts
from pipelines.annotation import generate_caption, generate_qa_pairs
from pipelines.export import export_dataset  # new export module

OUTPUT_BASE = Path("data/annotations")
OUTPUT_BASE.mkdir(parents=True, exist_ok=True)

def process_pdf(pdf_path: Path):
    """Process a single PDF and return dataset as list of dicts."""
    pdf_output_dir = OUTPUT_BASE / pdf_path.stem
    pdf_output_dir.mkdir(exist_ok=True)

    # 1️⃣ PDF → images
    images = ingest_pdfs(pdf_path)
    if not images:
        return []

    # 2️⃣ OCR → text
    ocr_texts = ocr_images(images)

    # 3️⃣ Alignment
    aligned_pairs = align_images_texts(images, ocr_texts)

    # 4️⃣ Annotation
    dataset = []
    for img_path, text, score in aligned_pairs:
        dataset.append({
            "image": str(img_path),
            "aligned_text": text,
            "similarity_score": score,
            "caption": generate_caption(text),
            "qa_pairs": generate_qa_pairs(text)
        })

    # 5️⃣ Export dataset (images + JSON) automatically
    export_dataset(dataset, pdf_path.stem)

    return dataset
