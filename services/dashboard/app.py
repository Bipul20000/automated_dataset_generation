import sys
from pathlib import Path
import streamlit as st
import math

# --- Add project root to sys.path ---
BASE = Path(__file__).resolve().parents[2]  # automated-dataset root
sys.path.append(str(BASE))

# --- Import pipeline after sys.path fix ---
from pipelines.run_pipeline import process_pdf

st.set_page_config(page_title="PDF Annotation Dashboard", layout="wide")
st.title("Automated PDF Annotation Dashboard")

UPLOAD_DIR = Path("data/uploads")
EXPORT_DIR = Path("data/exports")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    temp_path = UPLOAD_DIR / uploaded_file.name
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info("Processing PDF... Please wait.")
    dataset = process_pdf(temp_path)
    st.success("Processing complete!")

    # --- Grid layout for pages ---
    columns_per_row = 2  # you can change to 3 or 4 depending on screen
    for i in range(0, len(dataset), columns_per_row):
        cols = st.columns(columns_per_row)
        for j, page in enumerate(dataset[i:i + columns_per_row]):
            with cols[j]:
                st.markdown(f"### Page: {Path(page['image']).name}")
                if Path(page['image']).exists():
                    st.image(str(page['image']), use_column_width=True)
                st.markdown(f"**Caption:** {page['caption']}")
                st.markdown(f"**Similarity Score:** {page['similarity_score']:.4f}")
                st.markdown("**Q&A:**")
                for qa in page['qa_pairs']:
                    st.markdown(f"- Q: {qa['question']}")
                    st.markdown(f"  A: {qa['answer']}")

    # --- JSON download ---
    export_path = EXPORT_DIR / temp_path.stem / f"{temp_path.stem}_dataset.json"
    if export_path.exists():
        with open(export_path, "r", encoding="utf-8") as f:
            json_content = f.read()
        st.download_button(
            label="Download JSON",
            data=json_content,
            file_name=f"{temp_path.stem}_dataset.json",
            mime="application/json"
        )
        st.markdown(f"**Exported images + JSON folder:** `{EXPORT_DIR / temp_path.stem}`")
