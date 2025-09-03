from flask import Blueprint, request, jsonify, session,send_from_directory,current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.language_modifier.text_file_translator import TextFileTranslator
from src.language_modifier.csv_translator import CsvTranslator
from src.language_modifier.language_code_resource import create_lang_codes
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from src.user.user_translation_query import saved_files_query
from src.db.db_functions import insert_data
import logging

file_translation_bp = Blueprint("file_translation", __name__, template_folder='../pages')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]

def upload_file(): 
        if 'file' not in request.files:
            logging.info("No file submitted")
            return None, "No file submitted"
         
        if request.method == "POST":
            file = request.files['file']

        if file.filename == '':
            logging.info("File field is empty")
            return None, "File field is empty"
        
        if file.filename and not allowed_file(file.filename):
            logging.info(f"Please only submit these file types{current_app.config["ALLOWED_EXTENSIONS"]}")
            return None,(f"Please only submit these file types{current_app.config["ALLOWED_EXTENSIONS"]}")
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return file_path, None
        
@file_translation_bp.route('/translate_document', methods=['POST'] )
@jwt_required()
def translate_text_files():
    lang_codes = create_lang_codes()
    username = get_jwt_identity()

    if request.method == 'POST':
        file_path, error = upload_file()
        if not file_path:
            return jsonify({"error": error}), 400
        file = os.path.basename(file_path)
        target_language_name = request.form['target_language']
        
        for name, code in lang_codes.items():
            if target_language_name.lower() == name:
                target_language_code = code

        file_extension = os.path.splitext(file)[1].lower().lstrip('.')

        if file_extension.lower() == 'txt':
            translator = TextFileTranslator(file, target_language_code)
            translated_file = translator.save_txt_file()
            pass

        if file_extension.lower() == 'csv':
            translator = CsvTranslator(file, target_language_code)
            translated_file = translator.save_csv()
            pass
       
        if username:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            values = (username,file, translated_file,target_language_name, timestamp)
            query = saved_files_query()
            insert_data(query,values)
            pass

        return jsonify({
            "original file" : file,
            "download_name" : translated_file
            })


@file_translation_bp.route('/download_file', methods = ['GET'])
@jwt_required()
def download_file():


    filename = request.args.get('file')
    print("DEBUG: filename received:", filename)
    
    if not filename or not allowed_file(filename):
        return jsonify({
            "error": f"File was not submitted or has an invalid extension. "
                     f"Extensions allowed are {current_app.config['ALLOWED_EXTENSIONS']}."
        }), 400
    
    folder = current_app.config.get('TESTING_FOLDER') if current_app.config.get('TESTING') else current_app.config['UPLOAD_FOLDER']
    file_path = os.path.join(folder, filename)

    if not os.path.exists(file_path):
        return jsonify({
            "error": f"Incorrect filename. {filename} was not found on the server."
        }), 400
    
    verified_filename = secure_filename(filename)

    return send_from_directory(
        directory =os.path.abspath(folder) ,
        path=verified_filename,
        as_attachment=True,
        download_name=verified_filename
    )