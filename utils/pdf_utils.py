import fitz
import streamlit as st

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        st.error(f"Failed to open PDF: {e}")
        return ""
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text
