import csv
from language_modifier.base_translator import TranslatorCore
from language_modifier.language_translator import translate_text
import asyncio
import os
import logging

class CsvTranslator(TranslatorCore):
    
    def __init__(self, file_path, target_lang_code, upload_folder=None):
        super().__init__(file_path, target_lang_code, upload_folder=os.path.join(os.path.dirname(__file__), "") )

    def csv_reader(self):

        columns = []
        rows = []

        with open (self.upload_path, encoding="utf-8", newline = "") as csvfile:
            csvreader = csv.reader(csvfile)
            logging.info(f"Reading {self.upload_path}")

            columns = next(csvreader)
            for row in csvreader:
                if any(cell.strip() for cell in row):
                    rows.append(row)
            logging.info(f"{columns} + {rows} found in {self.file_path}")

        return columns, rows
    
    def translate_csv(self):
        self.file_validator()

        columns, rows = self.csv_reader()
    
        rows_str = "\n".join(["||".join(row) for row in rows])

        translated_text = asyncio.run(translate_text(rows_str, self.target_lang_code))
        logging.info("Translating csv file")

        translated_rows =[]

        # Removing whitespaces since translated text function generates them

        for row in translated_text.split("\n"):
            cells = row.split("||")
            cleaned_cell = [cell.strip() for cell in cells]
            translated_rows.append(cleaned_cell)
        
        logging.info(f"Translated rows are {translated_rows}")

        return columns, translated_rows
    
    def generate_csv(self):

        columns, translated_rows = self.translate_csv()  

        self.full_output_path = self.file_exists()

        if columns or translated_rows is None:
            return None
        if columns and translated_rows:
            with open(self.full_output_path, 'x',encoding="utf-8",newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)       
                    csvwriter.writerow(columns)             
                    csvwriter.writerows(translated_rows)
            return os.path.basename(self.full_output_path)

    def save_csv(self):
        translated_file = self.generate_csv()
        return translated_file
