import streamlit as st
import requests
import os
from utils.pdf_utils import extract_text_from_pdf
from utils.metadata_utils import extract_metadata
from utils.openalex_utils import fetch_and_compare
import pandas as pd


st.title("📄 Research Paper Recommender (PDF Upload or URL)")
st.markdown(
    """
Upload a PDF research paper **or provide a URL to an open-access PDF** to extract metadata and discover related open-access papers based on keyword similarity.

**Sample URL (open-access ArXiv PDF) already provided**  

"""
)


uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
pdf_url = st.text_input(
    "Or enter a PDF URL (must be open-access):",
    value="https://arxiv.org/pdf/2305.05084"
)


def fetch_pdf_from_url(url, temp_path="temp_url.pdf"):
    try:
        resp = requests.get(url, timeout=20)
        if resp.status_code != 200:
            st.error(f"Failed to fetch PDF. Status code: {resp.status_code}")
            return None
        if "application/pdf" not in resp.headers.get("Content-Type", ""):
            st.error("The URL does not point to a valid PDF.")
            return None
        with open(temp_path, "wb") as f:
            f.write(resp.content)
        return temp_path
    except Exception as e:
        st.error(f"Error fetching PDF: {e}")
        return None


if "metadata_extracted" not in st.session_state:
    st.session_state.metadata_extracted = False
    st.session_state.text = None
    st.session_state.authors = []
    st.session_state.institutions = []
    st.session_state.citations = []
    st.session_state.key_phrases = []

if st.button("📄 Extract Metadata"):
    pdf_path = None
    if uploaded_pdf:
        pdf_path = "uploaded.pdf"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_pdf.read())
    elif pdf_url:
        pdf_path = fetch_pdf_from_url(pdf_url)

    if pdf_path:
        with st.spinner("Extracting metadata..."):
            text, authors, institutions, citations, key_phrases = extract_metadata(pdf_path)

            # Store in session state for next button
            st.session_state.text = text
            st.session_state.authors = authors
            st.session_state.institutions = institutions
            st.session_state.citations = citations
            st.session_state.key_phrases = key_phrases
            st.session_state.metadata_extracted = True

        st.subheader("Extracted Metadata")
        st.write("**Authors:**", ", ".join(authors) if authors else "Not detected")
        st.write("**Institutions:**", ", ".join(institutions) if institutions else "Not detected")
        st.write("**Top Keywords:**", ", ".join(key_phrases))
        st.write(f"**References Extracted:** {len(citations)}")
    else:
        st.warning("Please upload a PDF or provide a valid PDF URL.")


if st.session_state.metadata_extracted:
    if st.button("🔍 Find Related Open Access Papers"):
        with st.spinner("Searching OpenAlex and comparing papers..."):
            results = fetch_and_compare(
                st.session_state.citations,
                st.session_state.key_phrases
            )

        if results:
            df = pd.DataFrame(results)
            st.subheader("Top 8 Recommended Papers (by Jaccard Similarity)")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No open-access related papers found.")
