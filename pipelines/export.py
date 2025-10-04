"""Export dataset to JSON/CSV
"""
from pathlib import Path
from typing import List, Dict
import json
import csv


def export_json(items: List[Dict], out_path: str):
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def export_csv(items: List[Dict], out_path: str):
    if not items:
        return
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    keys = sorted({k for it in items for k in it.keys()})
    with open(p, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for it in items:
            writer.writerow({k: it.get(k, '') for k in keys})


if __name__ == "__main__":
    print("export module - export_json / export_csv")
