from db_connector import *

def retrieve_data(query,column,one_row=True):    
    db  = Database()
    result = db.execute_query_fetch_data(query, (column,),one_row)
    return result

def retrieve_all(query,column):    
    db  = Database()
    result = db.execute_query_fetch_data(query, (column,))
    return result

def insert_data(query,values):
    db = Database()
    db.execute_query(query,values)

def delete_data(query):
    db = Database()
    db.execute_query(query)