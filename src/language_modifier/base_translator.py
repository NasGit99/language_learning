from flask import current_app
import os
import logging

class TranslatorCore():
    def __init__(self, file_path, target_lang_code, upload_folder=None):
        self.file_path = file_path
        self.upload_folder = upload_folder or current_app.config['UPLOAD_FOLDER']
        self.upload_path = os.path.join(self.upload_folder, file_path)
        self.target_lang_code = target_lang_code
        self.output_file = f"{self.target_lang_code}_{self.file_path}"
        self.full_output_path = os.path.join(self.upload_folder,self.output_file)

    def file_validator(self, func):
        try:
            return func()
        except FileNotFoundError:
            msg = f"Error: {self.file_path} not found, please make sure the file path is correct."
            logging.error(msg)
            raise FileNotFoundError(msg)
        except IOError as e:
            msg = f"Error: Unable to read the file {self.file_path}. Reason: {e}"
            logging.error(msg)
            raise IOError(msg)
        except Exception as e:
            msg = f"Unexpected error reading {self.file_path}. Reason: {e}"
            logging.error(msg)
            raise

    def file_exists(self,func):
        try:
            return func()
        except FileExistsError:
            print(f"Error: The file {self.output_file} already exists. Creating a new file")
            # If the file already exists, append a number to the file name    
            counter = 1
            base_name, ext = os.path.splitext(self.output_file)

            # Keep checking if the file exists, appending a number until it doesn't
            while os.path.exists(self.full_output_path):
                self.output_file = f"{base_name}_{counter}{ext}"
                # Redefining the full output path so it doesnt save over the original file
                self.full_output_path = os.path.join(self.upload_folder, self.output_file)
                os.path.join(self.upload_folder,self.output_file)
                counter += 1         
            # Create and write to the new unique file name
                return func()
        logging.info(f"{self.full_output_path} has been uploaded")
        return os.path.basename(self.output_file)