

def text_history_query():
    
    query = "INSERT INTO users_txt_history (USERNAME, SRC_TXT, DST_TXT, TARGET_LANG, SUBMITTED_AT) VALUES (%s,%s,%s,%s,%s)"

    return query

def saved_txt_query():

    query = "INSERT INTO users_saved_txt (USERNAME, SRC_TXT, DST_TXT, SUBMITTED_AT) VALUES (%s,%s,%s,%s)"

    return query

def saved_files_query():
    
    query = "INSERT INTO users_saved_files (USERNAME, ORIGINAL_FILE_NAME," \
    "TRANSLATED_FILE_NAME, TRANSLATED_LANG, SUBMITTED_AT) VALUES(%s,%s,%s,%s,%s)"

    return query