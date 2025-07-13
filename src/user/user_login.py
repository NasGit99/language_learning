import bcrypt
import secrets
from datetime import datetime
import sys
sys.path.append('../db/')
from db_functions import *

def insert_user_query():

    query ="""

    INSERT INTO users (username, email, first_name, last_name, password, created_at)
    VALUES (%s, %s, %s, %s, %s, %s);
        """   
    return query 

def retrieve_username_query():
    query = "select username from users where username = %s"
    return query

def retrieve_password_query():
    query = "select password from users where username = %s"
    return query

def hash_password(password):

    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_bytes, salt) 
    return password_hash

def decrypt_hash(password,stored_hash):
    # Checks the password against the hash
    password_bytes = password.encode("utf-8")
    hash_bytes = stored_hash.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hash_bytes)  

def validate_username(function):
    if function == "signup":
        while True:
            username = input("Type your username, max length is 16 characters: ")

            if len(username) > 16:
                print("Username is greater than 16 characters")
                continue

            validate_username = retrieve_data(retrieve_username_query(), username)

            if validate_username:
                print("Username already exists: Try again: ")
                continue
            else:
                break
        return username
    
    if function == "login":
        while True:
            username = input("Type your username, max length is 16 characters: ")

            if len(username) > 16:
                print("Username is greater than 16 characters")
                continue
            else:
                break
        return username

def validate_name(field):
    # Might seperate this later in case the names need seperate logic
    while True:
        if field == "fn":
            first_name = input("Type your first name:")
            name_field = first_name
        if field == "ln":
            last_name = input("Type your last name: ")
            name_field = last_name

        # Validates if there are any numbers or symbols
        if any(char.isnumeric() for char in name_field) or any(not char.isalnum() for char in name_field):
            print("Only letters are allowed. Try again! ")
            continue
        else:
            break 

    return name_field.capitalize()

def validate_password():
    while True:
        password = input("Enter Password, length > = 8")
        if len(password) <8:
            print("Password length is < 8")
            continue
        else:
            break
    return password

def validate_email():
    while True:
        email = input("Type in your email address! ")
        if "@" not in email:
            print("Incorrect email address")
            continue
        else:
            break 
    return email

def create_signup():
        username = validate_username("signup")
        first_name = validate_name("fn")
        last_name = validate_name("ln")
        email = validate_email()
        password = validate_password()    
        hashed_password = hash_password(password)
        timestamp = datetime.now()

        values = (username, email, first_name, last_name, hashed_password, timestamp)

        insert_users(insert_user_query(),values)
               
def create_login():
        
    while True:
        registered_user = validate_username("login")

        user_result = retrieve_data(retrieve_username_query(), registered_user)

        if user_result is None:
            print("Username not found")
            continue

        username = user_result[0]

        print("Username found: ", username)

        break

    while True:
            registered_password = input("Type password")
            password_result = retrieve_data(retrieve_password_query(), registered_user)
            
            if password_result is None:
                print("Could not find password, try again")
                # Future iterations could include a password attempt
                continue

            stored_hash = password_result[0]
            
            if not decrypt_hash(registered_password,stored_hash):
                print("Incorrect password, try again")
                continue
            else:
                print ("Successful login")
            return registered_user

create_login()