from flask import Blueprint, render_template, request, redirect, session, flash, url_for,send_from_directory,current_app
from src.language_modifier.text_file_translator import create_new_file
from src.language_modifier.language_code_resource import create_lang_codes
import os
from werkzeug.utils import secure_filename

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
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = (os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return file_path

#This will be used later for prompting the user to download the files
@file_translation_bp.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], name)  

@file_translation_bp.route('/translate_document', methods=['GET','POST'] )

def translate_text_files():
    lang_codes = create_lang_codes()

    if request.method == 'POST':
        file_path = upload_file()
        if not file_path:
            return redirect(url_for('file_translation.translate_text_files'))
        file = os.path.basename(file_path)
        target_language = request.form['target_language']
        # We will return the translated file object here
        translated_file = create_new_file(file, target_language)
        # ToDO: Add code so users can also download
    return render_template('document_translation.html',
                           languages=lang_codes)

