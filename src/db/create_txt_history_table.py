from db_connector import *

def create_txt_history_table():
   db = Database()
   query ="""
    CREATE TABLE IF NOT EXISTS users_txt_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    src_txt VARCHAR(2000) NOT NULL,
    dst_txt VARCHAR(2000),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );"""
   db.execute_query(query)
   

if __name__ == "__main__":
   create_txt_history_table()