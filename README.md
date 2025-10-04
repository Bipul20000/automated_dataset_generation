# Automated Dataset Scaffold

This repository provides a scaffold for building an automated dataset pipeline that converts PDF documents into image-based datasets with OCR, alignment, annotation, and export steps.

Structure

- data/                     # store test PDFs/images
- pipelines/
  - ingest.py               # pdf → images
  - ocr.py                  # OCR text extraction
  - alignment.py            # CLIP align text + images
  - annotation.py           # generate Q&A/captions
  - export.py               # dataset export (json/csv)
- services/
  - api/                    # FastAPI backend
  - dashboard/              # Streamlit dashboard
- requirements.txt
- .gitignore

Quick start

1. Create a virtual environment and install requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the API (example):

```bash
uvicorn services.api.main:app --reload
```

3. Run the dashboard (example):

```bash
streamlit run services/dashboard/app.py
```

Files are minimal stubs intended as a starting point.