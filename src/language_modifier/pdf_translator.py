from language_modifier.base_translator import TranslatorCore
from language_modifier.language_translator import translate_text,translate_bulk
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

        pdf_content = []

        for page in pdf:
            txt_page = page.get_textpage().extractDICT()["blocks"]
            logging.info(page)

            for block in txt_page:
                lines = block.get("lines")
                for line in lines:
                    spans = line.get("spans")
                    for metadata in spans:
                        # Need the BBOX for annotations. Need to keep the text with attr for inserting into page. Maybe page num
                        if metadata.get("text").strip():
                            new_row = []
                            new_row.append(metadata.get("text"))
                            new_row.append(metadata.get("font"))
                            new_row.append(metadata.get("size"))
                            new_row.append(metadata.get("color"))
                            new_row.append(metadata.get("bbox"))
                            new_row.append(page.number)
                            pdf_content.append(new_row)
                            logging.info(f"Metadata is: {new_row} ")

        return pdf, pdf_content
    
    def translate_pdf(self):

        pdf, pdf_content = self.pdf_text_extractor()
        self.full_output_path= self.file_exists()

        txt_src = ""

        for i in pdf_content:
            txt_src += i[0] + "|||"

        translated_content = asyncio.run(translate_text(txt_src,self.target_lang_code))
        
        translated_list = translated_content.split('|||')

        logging.info(f"Translated content is {translated_list}")

        for i, value in enumerate(pdf_content):
            if i < len(translated_list):
                i[0] = translated_list[value]
                
        #Creating annotations so we can remove the content to later replace it
        
        #TODO: Doesnt seem to be retaining bold letters and quotation marks

        for page in pdf:
            for attr in pdf_content:
                translations = attr[0]
                font = attr[1]
                size = attr[2]
                color = attr[3]
                bbox = attr[4]

                font = self.font_validator(font)
                color = self.color_validator(color)

                page.add_redact_annot(bbox,text=translations, fontname=font, fontsize=size, text_color=color)
                
                # Removes content 
                page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,graphics=pymupdf.PDF_REDACT_LINE_ART_NONE) 

        pdf.save(self.full_output_path)
        pdf.close()
        return os.path.basename(self.full_output_path)

    def font_validator(self,font_name):
            base_fonts = pymupdf.Base14_fontdict.keys()
            if font_name.lower() not in base_fonts:
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
