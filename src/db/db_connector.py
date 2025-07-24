from var import *
import mysql.connector
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Database():

   connection = None

   def __init__(self):
      if Database.connection is None:
         try:
            temp_conn = mysql.connector.connect(host=host, user=user, password=passwd)
            temp_cursor = temp_conn.cursor()
            temp_cursor.execute("CREATE DATABASE IF NOT EXISTS language_learning;")
            temp_conn.commit()
            temp_cursor.close()
            temp_conn.close()

            Database.connection = mysql.connector.connect(host=host, user=user, password=passwd, database ="language_learning")
         except Exception as error:
            print("Error: Connection not established {}".format(error))
         else:
            print("Connection established")
    
    #ToDO: reduce repetitive code
   
   def execute_query(self, sql, values=None):
    if Database.connection is None:
        print("Error: No active connection")
        return
    try:
        cursor = Database.connection.cursor()
        if values:
            cursor.execute(sql, values)
        else:
            cursor.execute(sql)
        Database.connection.commit()
        affected = cursor.rowcount
    except Exception:
        logging.error("Failed to execute query: %s", sql)
        logging.error("With values: %s", values)
        logging.exception("Exception occurred during cursor.execute()")
    else:
        logging.info(f"Query executed successfully. Rows affected: {affected}")
    finally:
        if cursor:
            cursor.close()
      
   def execute_query_fetch_one(self, sql, values=None):
    if Database.connection is None:
        print("Error: No active connection")
        return None
    try:
        cursor = Database.connection.cursor()
        if values:
            cursor.execute(sql, values)
        else:
            cursor.execute(sql)
        result = cursor.fetchone()  # fetch the single row
    except Exception:
        logging.error("Failed to execute query: %s", sql)
        logging.error("With values: %s", values)
        logging.exception("Exception occurred during cursor.execute()")
        return None
    else:
        affected = cursor.rowcount
        logging.info(f"Select query executed successfully. Rows affected: {affected}")
        return result
    finally:
        if cursor:
            cursor.close()
   

