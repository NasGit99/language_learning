from language_modifier.language_translator import *
import os
import asyncio
from flask import current_app
from language_modifier.base_translator import *
import logging

class FileTranslator(TranslatorCore):

    def __init__(self, file_path, target_lang_code, upload_folder=None):
        super().__init__(file_path, target_lang_code)

    def read_txt_file(self):
        with open(self.upload_path,"r", encoding="utf8") as file:
            # Handles multi line files and saves it as a list
            lines = file.readlines()
            return lines

    def translate_file(self):
        lines = self.file_validator(self.read_txt_file)
        if lines is None:
            return None

        raw_file =""
        
        # I have to transform the list into a string to send one single api request to improve processing
        for line in lines:
            raw_file += line + "|"

        translated_text = asyncio.run(translate_text(raw_file, self.target_lang_code))
        translated_lines = [line.strip() for line in translated_text.split("|")]
        
        content = []
        for original, translated in zip(lines, translated_lines):
            if not original.strip():
                continue
            content.append(original)
            if not translated.strip():
                continue
            content.append("Translation: " + translated.strip())
        return content
    
    def generate_txt_file(self):
        content = self.translate_file()
        # Prevents files that do not exist from being entered
        if content is None:
            return None
        if content:
            with open (self.full_output_path,"x", encoding="utf-8") as file:
                    for line in content:
                        file.write(line + '\n')

    def save_txt_file(self):
        self.file_exists(self.generate_txt_file)

