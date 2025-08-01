from src.language_modifier.language_translator import *
import os
import asyncio

def read_txt_file(file_path):
    try:
        with open(file_path,"r") as file:
            # Handles multi line files and saves it as a list
            lines = file.readlines()
            if not lines:
                print(f"The file {file_path}is empty")
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

    translated_text=[]

    for line in lines:
        # Ignores blank lines
        if not line.strip():
            continue
        translated_text.append(line.strip())
        translated_text.append("Translation: " + asyncio.run(translate_text(line,target_lang_code)))
    return translated_text

def create_new_file(file_path, target_lang_code):
    # Use the old file name and append the target language for naming

    output_file = f"{target_lang_code}_{file_path}"
    content = translate_file(file_path, target_lang_code)

    # Prevents files that do not exist from being entered
    if content is None:
        return None

    try:
        with open (output_file,"x", encoding="utf-8") as file:
            for line in content:
                file.write(line + '\n')
    except FileExistsError:
        print(f"Error: The file {target_lang_code}_{file_path} already exists. Creating a new file")

        # If the file already exists, append a number to the file name
        counter = 1
        base_name, ext = os.path.splitext(output_file)

        # Keep checking if the file exists, appending a number until it doesn't
        while os.path.exists(output_file):
            output_file = f"{base_name}_{counter}{ext}"
            counter += 1
        
        # Create and write to the new unique file name
        with open(output_file, "x", encoding="utf-8") as file:
            for line in content:
                file.write(line + '\n')


