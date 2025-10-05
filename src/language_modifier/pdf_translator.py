from language_modifier.base_translator import TranslatorCore
from language_modifier.language_translator import translate_text
import asyncio
import logging
import pymupdf

class PdfTranslator(TranslatorCore):
    
    def __init__(self, file_path, target_lang_code, upload_folder=None,username=None):
        super().__init__(file_path, target_lang_code, upload_folder)
        self.username = username

    # def font_validator()

    def pdf_txt_extractor(self):
        doc = pymupdf.open(self.file_path)
        for page in doc:
            txt_page = page.get_textpage().extractDICT()["blocks"]

            for block in txt_page:
                lines = block.get("lines")
                for line in lines:
                    spans = line.get("spans")
                    for metadata in spans:
                        text = metadata.get("text")
                        font = metadata.get("font")
                        size = metadata.get("size")
                        color = metadata.get("color")
                        origin = metadata.get("origin")
                        logging.info(f"""Metadata is: \n Text: {text}, 
                                     \n Font: {font}, 
                                     \n Size: {size}, 
                                     \n Color:{color}
                                     \n Origin:{origin}
                                                    """)

                        translated_text = asyncio.run(translate_text(text, self.target_lang_code))
                        logging.info(f"Translated Line: {translated_text}")

                        hits = page.search_for(text) # Finding areas to replace text
                        logging.info (f"These are the hits:{hits}")

                        for rect in hits:
                            logging.info(f"These are the rects {rect}")
                            page.add_redact_annot(rect)

                        # Removes content 
                        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE) 
                        # Replaces content with correct data 
                        page.insert_text(
                            origin,
                            translated_text,
                            fontname=font,
                            fontsize=size,
                            color=color,
                        )

            doc.save(self.output_file,deflate=True)

                
            #def translate_pdf(self):


