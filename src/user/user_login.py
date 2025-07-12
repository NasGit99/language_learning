import bcrypt
import secrets
from datetime import datetime
from create_user import *
from db.db_connector import *

#Remaining tasks: Create a db to store hashes

def db_connection(query):
    db = Database()

    db.execute_query(query)

def hash_password(password):

    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_bytes, salt) 
    return password_hash

def decrypt_hash(password,stored_hash):
    # Checks the inputted password against the hash
    password_bytes = password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, stored_hash)  

def validate_username():
    while True:
        username = input("Type your username, length is 16")
        if len(username) > 16:
            print("Length too long")
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

def insert_user_query():

    query ="""

    INSERT INTO users (username, email, first_name, last_name, password, created_at)
    VALUES (%s, %s, %s, %s, %s, %s);
        """
    

def create_signup():
    # Later on I can validate this user_list with the DB
    ## Check if user is in DB if not then allow creation
        username = validate_username()
        first_name = validate_name("fn")
        last_name = validate_name("ln")
        email = validate_email()
        password = validate_password()    
        hashed_password = hash_password(password)
        timestamp = datetime.now()

        user = User_Profile(username,first_name, last_name, email)

        values = (username, email, first_name, last_name, hashed_password, timestamp)

        query = db_connection(insert_user_query)
        
        
def create_login():

        registered_user = validate_username()

        while True:
            #ToDO fill this in with db objects
            if registered_user not in registered_password :
                print("Not registered, try again")
                continue
            else:
                break

        registered_password = input("Type password")

        # Here I will check the hash of the password to see if it matches registered_password

        while True:
            #This needs to be changed to grab the hash from the db
            stored_hash = "TODO"
            if not decrypt_hash(registered_password,stored_hash):
                print("Incorrect password, try again")
                continue
            else:
                break
        print ("Successful login")

        return registered_user

