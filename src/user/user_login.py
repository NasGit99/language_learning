import bcrypt
import secrets
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../db')))

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

def validate_username(function,username):
    if function == "signup":

        while True:
            if len(username) > 16:
                raise ValueError("Username is greater than 16 characters")

            validate_username = retrieve_data(retrieve_username_query(), username)

            if validate_username:
              raise ValueError("Username already exists: Try again: ")
            else:
                break
        return username
    
    if function == "login":
        while True:
            if len(username) > 16:
                raise ValueError("Username is greater than 16 characters")
            else:
                break
        return username

def validate_name(name):
    while True:
        name_field = name
        # Validates if there are any numbers or symbols
        if any(char.isnumeric() for char in name_field) or any(not char.isalnum() for char in name_field):
            raise ValueError("Only letters are allowed for name fields. Try again!")
        else:
            break 

    return name_field.capitalize()

def validate_password(password):
    while True:
        if len(password) <8:
            raise ValueError("Password length must be > 8")
        else:
            break
    return password

def validate_email(email):
    while True:
        if "@" not in email:
            raise ValueError("Email is not formatted properly!")
        else:
            break 
    return email
def user_validator(registered_user,password):
    password_result = retrieve_data(retrieve_password_query(), registered_user)
            
    if password_result is None:
        print("Could not find password, try again")
        # Future iterations could include a password attempt
        return None

    stored_hash = password_result[0]
    
    if not decrypt_hash(password,stored_hash):
        print("Incorrect password, try again")
        return None
    else:
        print ("Successful login")
    return registered_user

def create_signup(username,first_name,last_name, email, password):
        errors = {}
        
        try:
            username = validate_username("signup", username)
        except ValueError as e:
            errors['username'] = str(e)

        try:
            first_name = validate_name(first_name)
        except ValueError as e:
            errors['first_name'] = str(e)

        try:
            last_name = validate_name(last_name)
        except ValueError as e:
            errors['last_name'] = str(e)

        try:
            email = validate_email(email)
        except ValueError as e:
            errors['email'] = str(e)

        try:
            password = validate_password(password)
        except ValueError as e:
            errors['password'] = str(e)
        
        if errors:
            print("ERROR FOUND, not inserting")
            return None, errors
        # Added this so I could have better logging in tests
        print(f"NO ERRORS — running insert_data for {username} ")
        hashed_password = hash_password(password)
        timestamp = datetime.now()

        values = (username, email, first_name, last_name, hashed_password, timestamp)

        insert_data(insert_user_query(),values)

        return username, None
               
def create_login(username,password):
        
    while True:
        registered_user = validate_username("login",username)

        user_result = retrieve_data(retrieve_username_query(), registered_user)

        if user_result is None:
            print("Username not found")
            return None
        print(user_result)
        username = user_result[0]

        print("Username found: ", username)

        break

    while True:
        validated_user = user_validator(registered_user,password)
        return validated_user
            
