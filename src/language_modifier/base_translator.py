from flask import current_app
import os
import logging


class TranslatorCore():
    def __init__(self, file_path, target_lang_code, upload_folder=None):
        self.file_path = file_path
        self.upload_folder = upload_folder or current_app.config['UPLOAD_FOLDER']
        self.upload_path = os.path.join(self.upload_folder, file_path)
        self.target_lang_code = target_lang_code
        self.output_file =f"{self.target_lang_code}_{self.file_path}"
        self.new_output_file = ""
        self.full_output_path = os.path.join(self.upload_folder,self.output_file)


    def file_validator(self):

        if not os.path.exists(self.upload_path):
            msg = f"Error: {self.file_path} not found, please make sure the file path is correct."
            logging.error(msg)
            raise FileNotFoundError(msg)
        try:
            with open(self.upload_path, "r", encoding="utf-8"):
                pass  
        except IOError as e:
            msg = f"Error: Unable to read the file {self.file_path}. Reason: {e}"
            logging.error(msg)
            raise IOError(msg)
        except Exception as e:
            msg = f"Unexpected error reading {self.file_path}. Reason: {e}"
            logging.error(msg)
            raise RuntimeError(msg)

        return

    def file_exists(self):

        if not os.path.exists(self.full_output_path):
            return self.full_output_path
        
        counter = 1
        base_name, ext = os.path.splitext(self.output_file)

        while os.path.exists(self.full_output_path):
            self.new_output_file = f"{base_name}_{counter}{ext}"
            # Redefining the full output path so it doesnt save over the original file
            self.full_output_path= os.path.join(self.upload_folder, self.new_output_file)
            counter += 1
        return self.full_output_path
        

      