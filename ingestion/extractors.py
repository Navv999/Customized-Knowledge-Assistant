import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup



def extract_text_from_txt(file_path):
    """Reads text from a plain text file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_text_from_pdf(file_like_object):
    # Open the file-like object with PyMuPDF
    pdf_document = fitz.open(stream=file_like_object.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
        # print(text)   #full text extracted
    return text

def extract_text_from_url(url):
    try:
        response=requests.get(url,timeout=5)
        soup=BeautifulSoup(response.text,"lxml")
        paragraphs= [p.get_text() for p in soup.find_all("p")]
        return " ".join(paragraphs)[:2000]
    except Exception as e:
        return f"error fetching URL:{e}"

