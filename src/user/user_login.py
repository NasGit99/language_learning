import bcrypt
import secrets
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../db')))

from db_functions import *

class UserProfile:

    def __init__(self, username, email, first_name, last_name, password):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

    @staticmethod
    def insert_user_query():

        query ="""

        INSERT INTO users (username, email, first_name, last_name, password, created_at)
        VALUES (%s, %s, %s, %s, %s, %s);
            """   
        return query 
    
    @staticmethod
    def retrieve_username_query():
        query = "select username from users where username = %s"
        return query
    
    @staticmethod
    def retrieve_password_query():
        query = "select password from users where username = %s"
        return query
    
    @staticmethod
    def hash_password(password):

        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_bytes, salt) 
        return password_hash
    
    @staticmethod
    def decrypt_hash(password,stored_hash):
        # Checks the password against the hash
        password_bytes = password.encode("utf-8")
        hash_bytes = stored_hash.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hash_bytes)  
    
    @staticmethod
    def validate_username(function,username):
        if function == "signup":

            if len(username) > 16:
                raise ValueError("Username is greater than 16 characters")

            validate_username = retrieve_data(UserProfile.retrieve_username_query(), username)

            if validate_username:
                raise ValueError("Username already exists: Try again: ")
            
            return username
        
        if function == "login":
            if len(username) > 16:
                raise ValueError("Username is greater than 16 characters")
            
        return username
    
    @staticmethod
    def validate_name(name):
        name_field = name.strip()
        # Validates if there are any numbers or symbols
        if any(char.isnumeric() for char in name_field) or any(not char.isalpha() for char in name_field):
            raise ValueError("Only letters are allowed for name fields. Try again!")
        return name_field.capitalize()
    
    @staticmethod
    def validate_password(password):
        while True:
            if len(password) <8:
                raise ValueError("Password length must be > 8")
            else:
                break
        return password

    def validate_email(self):
            if "@" not in self.email:
                raise ValueError("Email is not formatted properly!")
            else:
                return self.email
            
    @staticmethod
    def user_validator(registered_user,password):
        password_result = retrieve_data(UserProfile.retrieve_password_query(), registered_user)
                
        if password_result is None:
            print("Could not find password, try again")
            # Future iterations could include a password attempt
            return None

        stored_hash = password_result[0]
        
        if not UserProfile.decrypt_hash(password,stored_hash):
            print("Incorrect password, try again")
            return None
        else:
            print ("Successful login")
        return registered_user

    def create_signup(self):
            errors = {}
            
            try:
                username = UserProfile.validate_username("signup", self.username)
            except ValueError as e:
                errors['username'] = str(e)

            try:
                first_name = self.validate_name(self.first_name)
            except ValueError as e:
                errors['first_name'] = str(e)

            try:
                last_name = self.validate_name(self.last_name)
            except ValueError as e:
                errors['last_name'] = str(e)

            try:
                email = self.validate_email()
            except ValueError as e:
                errors['email'] = str(e)

            try:
                password = self.validate_password(self.password)
            except ValueError as e:
                errors['password'] = str(e)
            
            if errors:
                print("ERROR FOUND, not inserting")
                return None, errors
            # Added this so I could have better logging in tests
            print(f"NO ERRORS — running insert_data for {username} ")
            hashed_password = self.hash_password(password)
            timestamp = datetime.now()

            values = (username, email, first_name, last_name, hashed_password, timestamp)

            insert_data(self.insert_user_query(),values)

            return self.username, None
    
    @staticmethod           
    def create_login(username,password):
            
        while True:
            registered_user = UserProfile.validate_username("login",username)

            user_result = retrieve_data(UserProfile.retrieve_username_query(), registered_user)

            if user_result is None:
                print("Username not found")
                return None
            print(user_result)
            username = user_result[0]

            print("Username found: ", username)

            break

        while True:
            validated_user = UserProfile.user_validator(registered_user,password)
            return validated_user
                
