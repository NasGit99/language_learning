from var import *
import mysql.connector

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

   def execute_query(self, sql):
      if Database.connection is None:
         print("Error: No active connection")
         return
      cursor = Database.connection.cursor()
      cursor.execute(sql)
      print("Query executed")
      cursor.close()
