import requests
import os
import time
from utils.pdf_utils import extract_text_from_pdf
from utils.metadata_utils import extract_keywords
from utils.similarity_utils import jaccard_similarity

def find_open_access_paper(citation_text):
    try:
        query = citation_text.split('“')[1].split('”')[0] if '“' in citation_text else citation_text[:150]
    except Exception:
        query = citation_text[:150]

    url = f"https://api.openalex.org/works?filter=open_access.is_oa:true&search={query}"
    resp = requests.get(url)
    if resp.status_code != 200:
        return None, None

    data = resp.json()
    if 'results' not in data or len(data['results']) == 0:
        return None, None

    work = data['results'][0]
    title = work.get('title')
    oa_info = work.get('open_access', {})
    pdf_url = oa_info.get('oa_url')
    return title, pdf_url

def fetch_and_compare(citations, base_keywords):
    base_keywords_set = set(k.lower().strip() for k in base_keywords)
    results = []

    for i, citation in enumerate(citations[:10]):  # limit for performance
        title, pdf_url = find_open_access_paper(citation)
        if pdf_url:
            pdf_url = pdf_url.replace("/abs/", "/pdf/")
            try:
                resp = requests.get(pdf_url, timeout=15)
                if resp.status_code == 200 and resp.headers.get("Content-Type", "").startswith("application/pdf"):
                    with open("temp.pdf", "wb") as f:
                        f.write(resp.content)
                    text = extract_text_from_pdf("temp.pdf")
                    os.remove("temp.pdf")

                    if len(text.strip()) < 500:
                        continue

                    ref_keywords = set(k.lower().strip() for k in extract_keywords(text, max_keywords=50, ngram=2))
                    similarity = jaccard_similarity(base_keywords_set, ref_keywords)
                    shared = ", ".join(sorted(base_keywords_set.intersection(ref_keywords)))

                    results.append({
                        "Title": title,
                        "PDF_URL": pdf_url,
                        "Similarity": round(similarity, 3),
                        "Shared Keywords": shared
                    })
            except Exception:
                continue
        time.sleep(2)

    results = sorted(results, key=lambda x: x["Similarity"], reverse=True)
    return results[:8]
