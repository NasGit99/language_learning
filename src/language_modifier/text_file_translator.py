from src.language_modifier.language_translator import *
import os
import asyncio
from flask import current_app

class FileTranslator():

    def __init__(self, file_path, target_lang_code, upload_folder=None):
        self.file_path = file_path
        self.upload_folder = upload_folder or current_app.config['UPLOAD_FOLDER']
        self.upload_path = os.path.join(self.upload_folder, file_path)
        self.target_lang_code = target_lang_code

    def read_txt_file(self):
        try:
            with open(self.upload_path,"r", encoding="utf8") as file:
                # Handles multi line files and saves it as a list
                lines = file.readlines()
                if not lines:
                    print(f"The file {self.file_path}is empty")
                    return None
                return lines
        except FileNotFoundError:
            print(f"Error: {self.file_path} not found, please make sure file path is correct.")
            return None
        except IOError as e:
            print(f"Error: Unable to read the file {self.file_path}. Reason: {e}")
            return None

    def translate_file(self):
        lines = self.read_txt_file()
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

    def create_new_file(self):
        # Use the old file name and append the target language for naming

        output_file = f"{self.target_lang_code}_{self.file_path}"
        content = self.translate_file()
        full_output_path = os.path.join(self.upload_folder, output_file)

        # Prevents files that do not exist from being entered
        if content is None:
            return None
        if content:
            try:
                with open (full_output_path,"x", encoding="utf-8") as file:
                    for line in content:
                        file.write(line + '\n')
            except FileExistsError:
                print(f"Error: The file {self.target_lang_code}_{self.file_path} already exists. Creating a new file")

        # If the file already exists, append a number to the file name    
                counter = 1
                base_name, ext = os.path.splitext(output_file)

                # Keep checking if the file exists, appending a number until it doesn't
                while os.path.exists(full_output_path):
                    output_file = f"{base_name}_{counter}{ext}"
                    # Redefining the full output path so it doesnt save over the original file
                    full_output_path = os.path.join(self.upload_folder, output_file)
                    counter += 1
                
                # Create and write to the new unique file name
                with open(full_output_path, "x", encoding="utf-8") as file:
                    for line in content:
                        file.write(line + '\n')
        return os.path.basename(output_file)
                


