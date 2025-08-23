def profile_data_query():
    query = "select username, first_name, last_name, email from users where username = %s Limit 15"
    return query

def user_translations_query():
    query = "select src_txt, dst_txt, target_lang, submitted_at from users_txt_history where username = %s and length(src_txt) >0 Limit 15"
    return query

def user_file_history_query():
    query ="select original_file_name, translated_file_name, translated_lang, submitted_at from users_saved_files where username = %s Limit 15"
    return query

def update_profile_query(column):
    query =f"UPDATE USERS SET {column} = %s where username =%s;"
    return query

def update_translation_username():
    query ="Update users_txt_history set username = %s where username = %s;"
    return query

def update_files_username():
    query ="Update users_saved_files set username = %s where username = %s;"
    return query