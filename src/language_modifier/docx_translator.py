from language_modifier.base_translator import TranslatorCore
from language_modifier.language_translator import translate_text
import asyncio
from docx import Document


class DocxTranslator(TranslatorCore):
    def __init__(self, file_path, target_lang_code, upload_folder=None, username=None, testing=None):
        super().__init__(file_path, target_lang_code, upload_folder,testing)
        self.username = username
    
    def doc_reader(self):
        doc = Document(self.upload_path)
        self.file_validator()
        # This can probably be cleaned up a bit for separate functions
        tbl_rows_str = ""

        for table in doc.tables:
            rows = table.rows

            for row in rows:
                for cell in row.cells:
                    tbl_rows_str += cell.text + "|||"

        paragraph_str = ""

        for paragraph in doc.paragraphs:
            paragraph_str += paragraph.text + "|||" 
        
        header_tbl_str = ""
        footer_tbl_str = ""
        header_text_str = ""
        footer_text_str = ""

        for section in doc.sections:
            # We can just define section.header section.footer than do the loops
            header_tbl= section.header.tables
            footer_tbl = section.footer.tables
            header_paragraphs = section.header.paragraphs
            footer_paragraphs = section.footer.paragraphs

            if header_tbl:
                for table in header_tbl:
                    rows = table.rows
                    for row in rows:
                        for cell in row.cells:
                            header_tbl_str += cell.text + "|||"

            if footer_tbl:
                for table in header_tbl:
                    rows = table.rows
                    for row in rows:
                        for cell in row.cells:
                            footer_tbl_str + "|||"
            
            if header_paragraphs:
                for paragraph in header_paragraphs:
                    header_text_str += paragraph.text + "|||"
            
            if footer_paragraphs:
                for paragraph in footer_paragraphs:
                    footer_text_str += paragraph.text + "|||"
                        
        return doc, tbl_rows_str, paragraph_str, header_tbl_str, footer_tbl_str, header_text_str, footer_text_str

    def translate_strings(self,text):
        translated_text = asyncio.run(translate_text(text,self.target_lang_code))
        return translated_text

    def translate_doc(self):
        doc, tbl_rows_str, paragraph_str, header_tbl_str, footer_tbl_str, \
        header_text_str, footer_text_str = self.doc_reader()

        translated_tbl_rows = self.translate_strings(tbl_rows_str)
        translated_paragraphs = self.translate_strings(paragraph_str)
        translated_header_tbl = self.translate_strings(header_tbl_str)
        translated_footer_tbl = self.translate_strings(footer_tbl_str)
        translated_header_text = self.translate_strings(header_text_str)
        translated_footer_text = self.translate_strings(footer_text_str)

        return doc, translated_tbl_rows, translated_paragraphs, translated_header_tbl, translated_footer_tbl, \
        translated_header_text, translated_footer_text

    def generate_doc(self):
        doc, translated_tbl_rows, translated_paragraphs, translated_header_tbl, translated_footer_tbl, \
        translated_header_text, translated_footer_text = self.translate_doc()

        new_tbl_rows = translated_tbl_rows.split("|||")
        cell_num = 0

        for table in doc.tables:
            rows = table.rows
            for row in rows:
                for cell in row.cells:
                    if cell_num < len(new_tbl_rows):
                        cell.text = new_tbl_rows[cell_num]
                        cell_num += 1
        
        new_paragraph_rows = translated_paragraphs.split("|||")
        paragraph_num = 0

        for paragraph in doc.paragraphs:
            if paragraph_num < len(new_paragraph_rows):
                paragraph.text = new_paragraph_rows[paragraph_num]
                paragraph_num += 1
        
        for section in doc.sections:
            header_tbl= section.header.tables
            footer_tbl = section.footer.tables
            header_paragraphs = section.header.paragraphs
            footer_paragraphs = section.footer.paragraphs

            new_header_tbl = translated_header_tbl
            new_footer_tbl = translated_footer_tbl
            new_header_txt = translated_header_text
            new_footer_txt = translated_footer_text

            header_tbl_num = 0
            footer_tbl_num = 0
            header_paragraphs_num = 0
            footer_paragraphs_num = 0


            if header_tbl:
                for table in header_tbl:
                    rows = table.rows
                    for row in rows:
                        for cell in row.cells:
                            if header_tbl_num < len(new_header_tbl):
                                cell.text = new_header_tbl[header_tbl_num]
                                header_tbl_num += 1

            if footer_tbl:
                for table in header_tbl:
                    rows = table.rows
                    for row in rows:
                        for cell in row.cells:
                            if footer_tbl_num < len(new_footer_tbl):
                                cell.text = new_footer_tbl[footer_tbl_num]
                                footer_tbl_num += 1
            
            if header_paragraphs:
                for paragraph in header_paragraphs:
                    if header_paragraphs_num < len(new_header_txt):
                        paragraph.text = new_header_txt[header_paragraphs_num]
                        header_paragraphs_num += 1
            
            if footer_paragraphs:
                for paragraph in footer_paragraphs:
                    if footer_paragraphs_num < len(new_footer_txt):
                        paragraph.text = new_footer_txt[footer_paragraphs_num]
                        footer_paragraphs_num +=1 
                        
        self.full_output_path= self.file_exists()
        doc.save(self.full_output_path)