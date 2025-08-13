from flask import Blueprint, render_template, session,request
from src.user.user_profile import profile_data_query, user_translations_query,user_file_history_query, update_profile_query, update_files_username, update_translation_username
from src.db.db_functions import insert_data, retrieve_all
from src.user.user_login import user_validator, hash_password

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

@user_profile_bp.route('/update_profile', methods=['GET','POST'] )

def update_profile():

    username = session.get('username')
    updated_fields = []

    profile_data = retrieve_all(profile_data_query(),username)
    
    _, db_first_name, db_last_name, db_email = profile_data[0]

    if request.method == "POST":
        new_username  = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        if old_password:
            user_validator(username,old_password)
            if user_validator:
                hashed_password = hash_password(new_password)
                values = (hashed_password, username)
                print("Updating password")
                insert_data(update_profile_query('password'),values)
                updated_fields.append("password")
        if first_name != db_first_name:
            print("Updating first name")
            values = (first_name, username)
            insert_data(update_profile_query('first_name'),values)
            updated_fields.append("first name")
        if last_name != db_last_name:
            print("Updating last name")
            values = (last_name, username)
            insert_data(update_profile_query('last_name'),values)
            updated_fields.append("last name")
        if email != db_email:
            print("Updating email address")
            values = (email, username)
            insert_data(update_profile_query('email'),values)
            updated_fields.append("email")
  
        # Updating the username associated with transactions so we can maintain the history
        values_user = (new_username, username)

        insert_data(update_translation_username(), values_user)
        print("Updating the translation history username")

        insert_data(update_files_username(),values_user )
        print("Updating the file translation history username")

        session['username'] = new_username

        # Resetting profile data
        profile_data = retrieve_all(profile_data_query(),username)
        return render_template('update_profile.html', profile=profile_data, updated_fields=updated_fields)
    
    return render_template('update_profile.html', profile=profile_data,updated_fields=updated_fields)
    