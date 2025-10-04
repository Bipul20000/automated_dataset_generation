# services/dashboard/app.py
import sys
from pathlib import Path
import streamlit as st
import requests
import importlib.util

# --- Project root ---
BASE = Path(__file__).resolve().parents[2]  # AUTOMATED-DATASET

# --- Dynamic import of pdf_to_images from pipelines/ingest.py ---
INGEST_PATH = BASE / "pipelines" / "ingest.py"
spec = importlib.util.spec_from_file_location("ingest", INGEST_PATH)
ingest = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ingest)
pdf_to_images = ingest.pdf_to_images  # function ready to use

# --- Unified upload directory (same as FastAPI) ---
UPLOAD_DIR = BASE / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

API_URL = "http://127.0.0.1:8000"  # FastAPI server URL

st.title("Automated Dataset Dashboard")

# --- PDF Upload Section ---
st.subheader("Upload PDF")
uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
    try:
        response = requests.post(f"{API_URL}/upload_pdf", files=files)
        if response.status_code == 200:
            st.success(f"Uploaded {uploaded_file.name} successfully!")

            # --- Convert PDF to images ---
            pdf_path = response.json()["path"]  # full path from API
            images_out_dir = Path(pdf_path).parent / f"{Path(pdf_path).stem}_images"
            out_files = pdf_to_images(pdf_path, images_out_dir)

            st.write("PDF converted to images:")
            for img_path in out_files:
                st.image(img_path, width=300)

        else:
            st.error(f"Upload failed: {response.json().get('error')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")

# --- List Uploaded PDFs ---
st.subheader("Uploaded PDFs & Image Folders")
try:
    response = requests.get(f"{API_URL}/list_uploads")
    if response.status_code == 200:
        files = [Path(f) for f in response.json().get("uploads", [])]
        if files:
            for f in files:
                st.markdown(f"**PDF:** {f.name}")
                # check if image folder exists
                img_folder = f.parent / f"{f.stem}_images"
                if img_folder.exists():
                    st.write("Preview of pages:")
                    for img_file in sorted(img_folder.iterdir()):
                        st.image(str(img_file), width=200)
                st.write("---")
        else:
            st.write("No PDFs uploaded yet.")
    else:
        st.error("Failed to fetch uploaded files from API")
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to API: {e}")
