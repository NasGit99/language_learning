from db_connector import *

def create_saved_file_table():
   db = Database()
   query ="""
    CREATE TABLE IF NOT EXISTS users_saved_files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL ,
    original_file_name TEXT NOT NULL,
    translated_file_name TEXT NOT NULL ,
    translated_lang TEXT  NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );"""
   db.execute_query(query)
   

if __name__ == "__main__":
   create_saved_file_table()