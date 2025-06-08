from flask import Blueprint, render_template, request, redirect, url_for
import sys
import os
from src.language_modifier.language_translator import *
from src.language_modifier.language_code_resource import *

main_bp = Blueprint("main", __name__, template_folder='../pages')


@main_bp.route('/', methods=['GET', 'POST'])
def process_text():
    lang_codes = create_lang_codes()

    if request.method == "POST":
        user_text = request.form['user_text']
        target_language = request.form['target_language']
        return redirect(url_for('main.process_text', user_text=user_text, target_language=target_language))

    user_text = request.args.get('user_text', '')
    target_language = request.args.get('target_language', '')
    transformed_text = ''

    if user_text and target_language:
        transformed_text = asyncio.run(translate_text(user_text, target_language))

    return render_template(
        'home.html',
        user_text=user_text,
        transformed_text=transformed_text,
        target_language=target_language,
        languages=lang_codes
    )
