# pipelines/export.py
from pathlib import Path
import json
import shutil

EXPORT_BASE = Path("data/exports")
EXPORT_BASE.mkdir(parents=True, exist_ok=True)

def export_dataset(dataset: list, pdf_name: str):
    """
    Exports processed dataset:
    - JSON file with all page info
    - Optional: copy images to structured folder
    """
    if not dataset:
        print(f"No data to export for {pdf_name}")
        return

    # Create folder for this PDF
    pdf_export_dir = EXPORT_BASE / pdf_name
    pdf_export_dir.mkdir(exist_ok=True)

    # Copy images to export folder and update paths in dataset
    for page in dataset:
        img_path = Path(page["image"])
        if img_path.exists():
            dest_img = pdf_export_dir / img_path.name
            shutil.copy(img_path, dest_img)
            page["image"] = str(dest_img)  # update path in dataset

    # Save JSON
    output_file = pdf_export_dir / f"{pdf_name}_dataset.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"Dataset exported for {pdf_name} → {output_file}")
