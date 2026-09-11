from pypdf import PdfReader
from docx import Document
import os


def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()


def extract_text_from_docx(filepath):
    document = Document(filepath)
    return "\n".join(
        paragraph.text for paragraph in document.paragraphs
    ).strip()


def extract_resume_text(filepath):
    extension = os.path.splitext(filepath)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(filepath)

    if extension == ".docx":
        return extract_text_from_docx(filepath)

    raise ValueError("Only PDF and DOCX resumes are supported.")
