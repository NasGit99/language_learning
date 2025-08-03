

def text_history():
    
    query = "INSERT INTO users_txt_history (USERNAME, SRC_TXT, DST_TXT, SUBMITTED_AT) VALUES (%s,%s,%s,%s)"

    return query

def saved_txt():

    query = "INSERT INTO users_saved_txt (USERNAME, SRC_TXT, DST_TXT, SUBMITTED_AT) VALUES (%s,%s,%s,%s)"

    return query

def saved_files():
    
    query = "INSERT INTO users_saved_files (USERNAME, ORIGINAL_FILE_NAME," \
    "TRANSLATED_FILE_NAME, TRANSLATED_LANG, SUBMITTED_AT) VALUES(%s,%s,%s,%s,%s)"

    return query