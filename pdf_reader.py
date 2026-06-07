from pypdf import PdfReader

def extract_text_from_pdf(uploaded_file):

    text = ""

    pdf_reader = PdfReader(uploaded_file)

    for page in pdf_reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text