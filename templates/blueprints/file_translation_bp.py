from flask import Blueprint, render_template, request, redirect, session, flash, url_for,send_from_directory,current_app
from src.language_modifier.text_file_translator import create_new_file
from src.language_modifier.language_code_resource import create_lang_codes
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from src.user.user_translations import saved_files
from src.db.db_functions import insert_data

file_translation_bp = Blueprint("file_translation", __name__, template_folder='../pages')
# I will update these extensions as more file functionality is introduced
ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file():
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return None
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file, please select a file for translation')
            return None
        if file.filename and not allowed_file(file.filename):
            flash("File type is not supported")
            return None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = (filename)
            file.save(file_path)
            return file_path

@file_translation_bp.route('/translate_document', methods=['GET','POST'] )

def translate_text_files():
    lang_codes = create_lang_codes()
    username = session.get('username')


    if request.method == 'POST':
        file_path = upload_file()
        if not file_path:
            return redirect(url_for('file_translation.translate_text_files'))
        file = os.path.basename(file_path)
        target_language = request.form['target_language']
        translated_file = create_new_file(file, target_language)
            
        if username:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            values = (username,file, translated_file,target_language, timestamp)
            query = saved_files()
            insert_data(query,values)
            pass

        return send_from_directory(
            directory=current_app.config["UPLOAD_FOLDER"],
            path=translated_file,
            as_attachment=True,
            download_name=translated_file
        )
    return render_template('document_translation.html',
                           languages=lang_codes,
                           )

