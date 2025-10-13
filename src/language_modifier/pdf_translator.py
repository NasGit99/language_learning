from language_modifier.base_translator import TranslatorCore
from language_modifier.language_translator import translate_text,translate_bulk
import asyncio
import logging
import pymupdf
import os
pymupdf.TOOLS.set_small_glyph_heights(True)

## Currently there is a limitation for PDFs with images. Only text can be processed

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

        for i, attr in enumerate(pdf_content):
            if i < len(translated_list):
                attr[0] = translated_list[i]

        new_pdf = pymupdf.open()

        for page_num, old_page in enumerate(pdf):
            rect = old_page.rect
            new_page = new_pdf.new_page(width=rect.width, height=rect.height)

            # Draw each text block belonging to this page
            for attr in pdf_content:
                text, font, size, color, bbox, pnum = attr
                if pnum == page_num:
                    font = self.font_validator(font)
                    color = self.color_validator(color)
                    html_text = f"""
                <div style="
                    font-family: {font};
                    font-size: {size}px;
                    color: rgb({int(color[0]*255)}, {int(color[1]*255)}, {int(color[2]*255)});
                    line-height: 1.1;
                    word-wrap: break-word;
                ">
                    {text}
                </div>
                """
                    # Expanding slightly to make sure text is writin within margins
                    rect = pymupdf.Rect(bbox)
                    rect.x0 -= 1.0     # expand left
                    rect.x1 += 1.0     # expand right
                    rect.y0 -= 0.8     # expand upward
                    rect.y1 += 0.8     # expand downward
                    new_page.insert_htmlbox(rect,html_text)
                    
        new_pdf.save(self.full_output_path)
        new_pdf.close()
        pdf.close()
        return os.path.basename(self.full_output_path)

    def font_validator(self, font_name):
        if "Bold" in font_name:
            return "Helvetica-Bold"
        elif font_name.lower() in pymupdf.Base14_fontdict.keys():
            return font_name
        else:
            logging.warning(f"Font '{font_name}' not found. Using Helvetica.")
            return "Helvetica"
            
    def color_validator(self, color_int):
        try:
            r = ((color_int >> 16) & 255) / 255
            g = ((color_int >> 8) & 255) / 255
            b = (color_int & 255) / 255
            return (r, g, b)
        except Exception:
            logging.warning(f"Invalid color value detected: {color_int}. Defaulting to black.")
            return (0, 0, 0)
