import streamlit as st
import pandas as pd
import os
import time

from utils.pdf_utils import extract_text_from_pdf
from utils.metadata_utils import extract_metadata
from utils.openalex_utils import fetch_and_compare

# ---------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------
st.title("📄 Research Paper Recommender (Text Mining + Jaccard Similarity)")
st.markdown(
    "Upload a PDF research paper to extract metadata and discover related open-access papers based on keyword similarity."
)

uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_pdf:
    temp_path = "uploaded.pdf"
    with open(temp_path, "wb") as f:
        f.write(uploaded_pdf.read())

    with st.spinner("Extracting metadata..."):
        text, authors, institutions, citations, key_phrases = extract_metadata(temp_path)

    st.subheader("Extracted Metadata")
    st.write("**Authors:**", ", ".join(authors) if authors else "Not detected")
    st.write("**Institutions:**", ", ".join(institutions) if institutions else "Not detected")
    st.write("**Top Keywords:**", ", ".join(key_phrases))
    st.write(f"**References Extracted:** {len(citations)}")

    if citations:
        if st.button("🔍 Find Related Open Access Papers"):
            with st.spinner("Searching OpenAlex and comparing papers..."):
                results = fetch_and_compare(citations, key_phrases)

            if results:
                df = pd.DataFrame(results)
                st.subheader("Top 8 Recommended Papers (by Jaccard Similarity)")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No open-access related papers found.")
