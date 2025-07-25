

# Text History

def text_history():
    
    query = "INSERT INTO users_txt_history (USERNAME, SRC_TXT, DST_TXT, SUBMITTED_AT) VALUES (%s,%s,%s,%s)"

    return query

# Save feature

def saved_txt():

    query = "INSERT INTO users_saved_txt (USERNAME, SRC_TXT, DST_TXT, SUBMITTED_AT) VALUES (%s,%s,%s,%s)"

    return query


# File History
