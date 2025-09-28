import re
import requests
from io import BytesIO
from PyPDF2 import PdfReader

def extract_pdf_sections(url, chunk_size=1800, min_chunk=50):
    """
    Pobiera PDF z URL i dzieli go na sekcje tekstowe.
    """
    resp = requests.get(url)
    resp.raise_for_status()

    reader = PdfReader(BytesIO(resp.content))
    full_text = ""

    for page in reader.pages:
        page_text = page.extract_text() or ""
        page_text = re.sub(r'\s+', ' ', page_text).strip()
        full_text += page_text + "\n"

    paragraphs = re.split(r'(?<=[.!?])\s+', full_text)
    sections, buffer = [], ""

    for p in paragraphs:
        if len(buffer) + len(p) <= chunk_size:
            buffer += p + " "
        else:
            if len(buffer.strip()) >= min_chunk:
                sections.append(buffer.strip())
            buffer = p + " "

    if len(buffer.strip()) >= min_chunk:
        sections.append(buffer.strip())

    return sections
