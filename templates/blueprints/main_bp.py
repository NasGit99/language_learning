from flask import Blueprint, request,jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.language_modifier.language_translator import *
from src.language_modifier.language_code_resource import *
from flask_jwt_extended import create_access_token
from src.user.user_login import UserProfile
from src.user.user_translation_query import text_history_query
from datetime import datetime,timedelta

from src.db.db_functions import *
import asyncio

main_bp = Blueprint("main", __name__, template_folder='../pages')

@main_bp.route('/signup', methods=['POST'])
def signup():
    errors = {}
    form = request.get_json()

    if request.method == "POST":
        username = form['username']
        first_name = form['first_name']
        last_name = form['last_name']
        email = form['email']
        password = form['password']

        user = UserProfile(username, email, first_name, last_name, password)

        user, errors = user.create_signup()

        if user:
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token)
        if errors:
            return jsonify(errors)

@main_bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        form = request.get_json()
        username = form['username']
        password = form['password']

        login_result = UserProfile.create_login(username, password)
        # This is for if the user needs more tokens
        if login_result:
            access_token = create_access_token(identity=username, expires_delta=timedelta(hours=1))
            refresh_token = create_access_token(identity=username, expires_delta=timedelta(days=7)) 
            return jsonify(access_token=access_token, refresh_token=refresh_token)
        else:
            return "Invalid credentials", 400


@main_bp.route('/translate_text', methods=['POST'])
@jwt_required()
def process_text():
    lang_codes = create_lang_codes()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if request.method == "POST":
        form = request.get_json()
        user_text = form['user_text']
        target_language_code = form['target_language']
        try:
            target_language_name = lang_codes[target_language_code.lower()]
        except KeyError:
            return jsonify({"error": "Invalid language code"}), 400

        if user_text and target_language_code:
            transformed_text = asyncio.run(translate_text(user_text, target_language_name))
            print(transformed_text)

    username = get_jwt_identity()
    
    if username:
        values = (username, user_text, transformed_text, target_language_name, timestamp)
        query = text_history_query()

        insert_data(query,values)
        pass

    return jsonify({
        "Original text" :user_text,
        "Translated Text":transformed_text,
        "Target Language": target_language_name
    }
    )


