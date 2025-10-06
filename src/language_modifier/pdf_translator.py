from language_modifier.base_translator import TranslatorCore
from language_modifier.language_translator import translate_text
import asyncio
import logging
import pymupdf
import os

class PdfTranslator(TranslatorCore):
    def __init__(self, file_path, target_lang_code, upload_folder=None, username=None, testing=None):
        super().__init__(file_path, target_lang_code, upload_folder,testing)
        self.username = username

    def pdf_reader(self):
        self.file_validator()
        pdf = pymupdf.open(self.upload_path)
        return pdf

    def pdf_text_extractor(self):
        pdf = self.pdf_reader()
        pdf_content = {"text":[],
                       "font": [],
                       "size": [],
                       "color": [],
                       "origin":[]}
        #TODO: Also grab page to reduce scrambling of words
        
        for page in pdf:
            txt_page = page.get_textpage().extractDICT()["blocks"]

            for block in txt_page:
                lines = block.get("lines")
                for line in lines:
                    spans = line.get("spans")
                    for metadata in spans:
                        pdf_content["text"].append(metadata.get("text"))
                        pdf_content["font"].append(metadata.get("font"))
                        pdf_content["size"].append(metadata.get("size"))
                        pdf_content["color"].append(metadata.get("color"))
                        pdf_content["origin"].append(metadata.get("origin"))
                        logging.info(f"""Metadata is: \n Text: {pdf_content["text"]}, 
                                     \n Font: {pdf_content["font"]}, 
                                     \n Size: {pdf_content["size"]}, 
                                     \n Color:{pdf_content["color"]}
                                     \n Origin:{pdf_content["origin"]}
                                                    """)
        return pdf, pdf_content
    
    def translate_pdf(self):
        pdf, pdf_content = self.pdf_text_extractor()
        self.full_output_path= self.file_exists()

        for text,font,size,color,origin in zip(
            pdf_content["text"],
            pdf_content["font"],
            pdf_content["size"],
            pdf_content["color"],
            pdf_content["origin"]) :
            #TODO: Translate function is running for each line causing slow processing
            translated_text = asyncio.run(translate_text(text, self.target_lang_code))

            for page in pdf:
                logging.info(f"Translated Line: {translated_text}")

                hits = page.search_for(text) # Finding areas to replace text
                logging.info (f"These are the hits:{hits}")

                for rect in hits:
                    page.add_redact_annot(rect)
                
                font = self.font_validator(font)
                color = self.color_validator(color)
                #TODO: Replace this with the page from our pdf_content so we can save it correctly
                # Removes content 
                page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,graphics=pymupdf.PDF_REDACT_LINE_ART_NONE) 
                # Replaces content with correct data 
                page.insert_text(
                    origin,
                    translated_text,
                    fontname=font,
                    fontsize=size,
                    color=color,
                )

        pdf.save(self.full_output_path)
        pdf.close()
        return os.path.basename(self.full_output_path)

    def font_validator(self,font_name):
            base_fonts = pymupdf.Base14_fontdict.keys()

            if font_name not in base_fonts:
                logging.warning(f"Font '{font_name}' is not a Base14 font.")
                return "Helvetica"
            else:
                return font_name
            
    def color_validator(self, color_int):
        try:
            r = ((color_int >> 16) & 255) / 255
            g = ((color_int >> 8) & 255) / 255
            b = (color_int & 255) / 255
            return (r, g, b)
        except Exception:
            logging.warning(f"Invalid color value detected: {color_int}. Defaulting to black.")
            return (0, 0, 0)
