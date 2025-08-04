from flask import Blueprint, render_template, session
from src.user.user_profile import profile_data_query, user_translations_query,user_file_history_query
from src.db.db_functions import retrieve_data, retrieve_all

user_profile_bp = Blueprint("user_profile", __name__, template_folder='../pages')

@user_profile_bp.route('/profile')

def create_profile():
    username = session.get('username')

    if username:
        profile_data = retrieve_all(profile_data_query(),username)
        translation_history = retrieve_all(user_translations_query(),username)
        file_translation_history =retrieve_all(user_file_history_query(), username)
        return render_template('user_profile.html',profile=profile_data, 
                               translation_history=translation_history, file_translation_history = file_translation_history)