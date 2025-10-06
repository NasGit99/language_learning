import os
import sys
import pytest
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.language_modifier.pdf_translator import PdfTranslator

test_dir = os.path.join(os.path.dirname(__file__), "") 
os.makedirs(test_dir, exist_ok=True)

test_file_1_name ="test_file_1.pdf"
test_file_1_path = os.path.join(test_dir, test_file_1_name)


@pytest.fixture(scope="session",autouse=True)
def create_pdf_file():
    c = canvas.Canvas(test_file_1_path, pagesize=letter)
    width, height = letter

    # --- Header ---
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 40, "This is the Header")

    # --- Body text ---
    c.setFont("Helvetica", 12)
    c.drawString(72, height - 100, "Hello! This is the body of the PDF.")
    c.drawString(72, height - 120, "You can add more lines of text here as needed.")
    c.drawString(72, height - 140, "The body is positioned between the header and footer.")

    # --- Footer ---
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(width / 2, 30, "This is the Footer - Page 1")
    c.save()

class TestInput():
    def test_pdf_translation(self):
        file_1 = PdfTranslator(test_file_1_name, "Spanish", test_dir,testing=True )
        output = file_1.translate_pdf()
        assert os.path.exists(os.path.join(test_dir, output))
        
    # def test_small_pdf_translation(self):
    #     file_1 = PdfTranslator("sample-local-pdf.pdf", "Spanish", test_dir,testing=True )
    #     output = file_1.translate_pdf()
    #     assert os.path.exists(os.path.join(test_dir, output))

