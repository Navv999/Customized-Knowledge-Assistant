import pymupdf as pdr
import fitz
def extract_text_from_pdf(pdf_path):
    with pdr.open(pdf_path) as doc:
        text=""
        for page in doc:
            text+=page.get_text()
    return text