import re
import spacy
import yake
from utils.pdf_utils import extract_text_from_pdf
from spacy.cli import download
try:
    nlp = spacy.load("en_core_web_sm")
except:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_authors_institutions(text):
    doc = nlp(text[:3000])
    authors = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    institutions = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    return list(set(authors)), list(set(institutions))

def extract_references(text):
    header_match = re.search(r'(?im)\b(?:references|bibliography)\b', text)
    if not header_match:
        return []
    refs_text = text[header_match.end():]
    refs_text = refs_text.replace('\r\n', '\n').replace('\r', '\n')
    refs_text = re.sub(r'\n{2,}', '\n', refs_text)
    refs_text = re.sub(r'\n(?!\s*(?:\[\s*\d+\s*\]|\d+\.\s*|\(\s*\d+\s*\)))', ' ', refs_text)
    pattern = r'((?:\[\s*\d+\s*\]|\d+\.\s*|\(\s*\d+\s*\))\s*.+?)(?=(?:\[\s*\d+\s*\]|\d+\.\s*\|\(\s*\d+\s*\))|$)'
    matches = re.findall(pattern, refs_text, flags=re.DOTALL)
    citations = [re.sub(r'\s+', ' ', m).strip() for m in matches]
    return citations

def extract_keywords(text, max_keywords=15, ngram=2):
    kw_extractor = yake.KeywordExtractor(lan="en", n=ngram, top=max_keywords)
    keywords = kw_extractor.extract_keywords(text)
    return [kw for kw, _ in keywords]

def extract_metadata(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    authors, institutions = extract_authors_institutions(text)
    citations = extract_references(text)
    key_phrases = extract_keywords(text, max_keywords=50, ngram=2)
    return text, authors, institutions, citations, key_phrases
