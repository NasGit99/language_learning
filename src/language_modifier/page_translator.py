from text_translator import *
import datetime
import os

def read_txt_file(file_path):
    try:
        with open(file_path,"r") as file:
            # Handles multi line files and saves it as a list
            lines = file.readlines()
            if not lines:
                print("The file {file_path}is empty")
                return None
            return lines
    except FileNotFoundError:
        print(f"Error: {file_path} not found, please make sure file path is correct")
        return None
    except IOError as e:
        print(f"Error: Unable to read the file {file_path}. Reason: {e}")
        return None

def translate_file(file_path, target_lang_code):
    lines = read_txt_file(file_path)
    if lines is None:
        return None

    translated_text = [translate_text(line.strip(),target_lang_code) for line in lines]
    return translated_text

def create_new_file(file_path, target_lang_code):
    # Use the old file name and append the target language for naming

    file_name = f"{target_lang_code}_{file_path}"
    content = translate_file(file_path, target_lang_code)

    # Prevents files that do not exist from being entered
    if content is None:
        return None

    try:
        with open (file_name,"x") as file:
            for lines in content:
                file.write(lines + '\n')
    except FileExistsError:
        print(f"Error: The file {target_lang_code}_{file_path} already exists. Creating a new file")

        # If the file already exists, append a number to the file name
        counter = 1
        base_name, ext = os.path.splitext(file_name)

        # Keep checking if the file exists, appending a number until it doesn't
        while os.path.exists(file_name):
            file_name = f"{base_name}_{counter}{ext}"
            counter += 1
        
        # Create and write to the new unique file name
        with open(file_name, "x", encoding="utf-8") as file:
            content = translate_file(file_path, target_lang_code)
            for line in content:
                file.write(line + '\n')

if __name__ == "__main__":
    # ToDo either in the UI or CLI, add code so user can check lang codes. 
    # ToDo add code to also validate file in this step and make sure the path is correct before proceeding
    file = input("Type the name of your file:")
    lang_code = input("Type the name of the language you want to translate the file to: ")

    create_new_file(file,lang_code)