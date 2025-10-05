from language_modifier.base_translator import TranslatorCore
from language_modifier.language_translator import translate_text
import asyncio
import logging
import pymupdf

class PdfTranslator(TranslatorCore):
    
    def __init__(self, file_path, target_lang_code, upload_folder=None,username=None):
        super().__init__(file_path, target_lang_code, upload_folder)
        self.username = username

    # Will add in code to exclude headers and footers later possibly

    def pdf_txt_extractor(self):
        doc = pymupdf.open(self.file_path)
        for page in doc:
            txt_page = page.get_textpage()
            logging.info(f"This is the text object confirmed: {txt_page}")

            txt_src = txt_page.extractText().split("\n")
            logging.info(f"Source text is here: \n {txt_src}")

            for line in txt_src:
                if not line.strip():
                    continue

                translated_text = asyncio.run(translate_text(line, self.target_lang_code))
                logging.info(f"Translated Line: {translated_text}")

                hits = page.search_for(line) # Finding rectangles to replace text
                logging.info (f"These are the hits:{hits}")

                for rect in hits:
                    logging.info(f"These are the rects {rect}")
                    # Also need to grab the font and size of the text for later possibly
                    page.add_redact_annot(rect, text=translated_text)
        
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE) 

        doc.save(self.output_file,deflate=True)

         
    #def translate_pdf(self):


