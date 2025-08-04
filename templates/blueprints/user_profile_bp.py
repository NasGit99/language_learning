from flask import Blueprint, render_template, session
from src.user.user_profile import profile_data_query
from src.db.db_functions import retrieve_data

user_profile_bp = Blueprint("user_profile", __name__, template_folder='../pages')

@user_profile_bp.route('/profile')

def create_profile():
    username = session.get('username')

    if username:
        profile_data = retrieve_data(profile_data_query(),username)
        print(profile_data)
        return render_template('user_profile.html',profile=profile_data )