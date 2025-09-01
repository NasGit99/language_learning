from flask import Blueprint, render_template,request,jsonify
from src.user.user_profile_query import profile_data_query, user_translations_query,user_file_history_query, update_profile_query, update_files_username, update_translation_username
from src.db.db_functions import insert_data, retrieve_all
from src.user.user_login import UserProfile
from flask_jwt_extended import jwt_required,get_jwt_identity,create_access_token
from datetime import timedelta
import logging


user_profile_bp = Blueprint("user_profile", __name__, template_folder='../pages')

@user_profile_bp.route('/profile')
@jwt_required()
def create_profile():
    username = get_jwt_identity()

    if username:
        profile_data = retrieve_all(profile_data_query(),username)
        if len(profile_data) == 0:
            return jsonify(f"Username : {username}, does not have any data associated with it. You may have changed your username recently please use the /login endpoint to get a new token")
        translation_history = retrieve_all(user_translations_query(),username)
        file_translation_history =retrieve_all(user_file_history_query(), username)
        return jsonify({"User Profile": profile_data, 
                        "Translation_history": translation_history,
                            "File_translation_history" : file_translation_history
                               })

@user_profile_bp.route('/update_profile', methods=['PATCH'] )
@jwt_required()
def update_profile():

    username = get_jwt_identity()
    updated_fields = []

    profile_data = retrieve_all(profile_data_query(),username)

    if not profile_data:
        return jsonify({"msg": "User not found"}), 404
    
    _, db_first_name, db_last_name, db_email = profile_data[0]

    if request.method == "PATCH":
        form = request.get_json()
        new_username  = form.get('new_username')
        first_name    = form.get('new_first_name')
        last_name     = form.get('new_last_name')
        email         = form.get('new_email')
        old_password  = form.get('old_password')
        new_password  = form.get('new_password')

        if new_password and not old_password:
            return jsonify("To update to a new password you need to send the old_password"), 400
        if new_password:
            if new_password != old_password:
                valid_user = UserProfile.user_validator(username,old_password)
                if valid_user:
                    hashed_password = UserProfile.hash_password(new_password)
                    values = (hashed_password, username)
                    logging.info("Updating password")
                    insert_data(update_profile_query('password'),values)
                    updated_fields.append("password")
                else:
                    logging.info("Validation failed")
                    return jsonify("Validation failed"),400
        if first_name:
            if first_name != db_first_name:
                logging.info(f"Updating first name to {first_name}")
                values = (first_name, username)
                insert_data(update_profile_query('first_name'),values)
                updated_fields.append("first name")
        if last_name:
            if last_name != db_last_name:
                logging.info(f"Updating last name to {last_name}")
                values = (last_name, username)
                insert_data(update_profile_query('last_name'),values)
                updated_fields.append("last name")
        if email:
            if email != db_email:
                logging.info(f"Updating email address to {email}")
                values = (email, username)
                insert_data(update_profile_query('email'),values)
                updated_fields.append("email")
        if new_username:
            if new_username != username:
                user_values = (new_username, username)
                # Updating the username associated with transactions so we can maintain the history
                insert_data(update_translation_username(), user_values)
                logging.info("Updating the translation history username")

                insert_data(update_files_username(),user_values )
                logging.info("Updating the file translation history username")

                insert_data(update_profile_query('username'),user_values)
                logging.info(f"Updating the username to {new_username}")

                # A new access token is given for username changes. 
                # To retrieve user information please use new access token or get a refresh token
                updated_fields.append("username")

                new_access_token = create_access_token(identity=new_username, expires_delta=timedelta(hours=1))
                logging.info(f"New access token has been granted to {new_username}. Old username was {username}")
                return jsonify ({"new_access_token(1 hour) due to name change": new_access_token,"updated_fields": updated_fields,
                                "msg": "Request a refresh token through the /login endpoint for longer access"})
            
        return jsonify({"updated_fields": updated_fields})