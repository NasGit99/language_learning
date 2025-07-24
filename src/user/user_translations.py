from create_user import *
from datetime import datetime


# Text History

def text_history():
    
    query = "INSERT INTO user_txt_history (USERNAME, SRC_TXT, DEST_TXT, SUBMITTED_AT) VALUES (%s,%s,%s,%s,%s)"

    return query

# Save feature

def saved_txt():

    query = "INSERT INTO user_saved_txt (USERNAME, SRC_TXT, DEST_TXT, SUBMITTED_AT) VALUES (%s,%s,%s,%s,%s)"

    return query


# File History
