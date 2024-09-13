import fitz  # PyMuPDF

def extract_text_from_pdf(file_like_object):
    # Open the file-like object with PyMuPDF
    pdf_document = fitz.open(stream=file_like_object.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text
