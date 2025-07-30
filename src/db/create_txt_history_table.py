from db_connector import *

def create_txt_history_table():
   db = Database()
   query ="""
    CREATE TABLE IF NOT EXISTS users_txt_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    src_txt TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    dst_txt TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );"""
   db.execute_query(query)
   

if __name__ == "__main__":
   create_txt_history_table()