# Research Paper Recommender – Text Mining & Open Access Discovery

## Project Overview

This project provides a **Streamlit-based web application** that allows you to explore academic papers efficiently. Users can either **upload a PDF** or **provide a URL to an open-access PDF**, and the app will extract key metadata and suggest related papers.

The application is designed to **save time, enhance literature discovery, and assist in research workflows**.

---

## Text Mining Aspect

The app uses **Natural Language Processing (NLP)** to analyze uploaded PDFs and extract valuable information:

* **Author & Institution Extraction**: Automatically identifies authors and affiliations from the paper.
* **Keyword Extraction**: Uses **YAKE (Yet Another Keyword Extractor)** to extract top keywords and key phrases.
* **Reference Extraction**: Detects references and bibliographic entries from the paper using regex.

This allows users to get a **quick summary of a paper’s content and context** without manually reading the entire document.

---

## Recommender System Aspect

Based on the extracted **keywords and references**, the app connects to the **OpenAlex API** to find **related open-access research papers**.

* Computes **Jaccard similarity** between keywords in the uploaded paper and candidate papers.
* Recommends the **top 8 papers** that share the most keywords.
* Helps users discover relevant literature quickly and efficiently.

---

## Usage

1. Go to the **Streamlit app**: [RS-TM Project](https://rs-tm-project.streamlit.app/)
2. Upload a PDF or enter a **URL to an open-access PDF** (e.g., `https://arxiv.org/pdf/2305.05084`).
3. Click **“Extract Metadata”** to see authors, institutions, keywords, and references.
4. Click **“Find Related Open Access Papers”** to get recommended papers based on keyword similarity.

---

## Technologies Used

* **Python 3.13**
* **Streamlit** – interactive web UI
* **spaCy** – NLP for entity extraction
* **YAKE** – keyword extraction
* **PyMuPDF** – PDF text extraction
* **OpenAlex API** – open-access research paper discovery

---

## Live Demo

Access the live app here: [RS-TM Project](https://rs-tm-project.streamlit.app/)
