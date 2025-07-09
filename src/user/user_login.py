import hashlib
from create_user import *

# In order to create the login I know the following:
## Need to either create or login
## Username has to be in a dictionary, or some other system
## hash password and match it if user exists, if not create a new one
## If it fails then return error
# Validations for fields needs to be done as well 

def create_login():
    # Later on I can validate this user_list with the DB
    user_list = {"user":"pass"}

    while True:
        user_input = input("Signup or Login: ")
        if user_input.lower() not in ("signup","login"):
            print("Incorrect option")
            continue
        else:
            break

    if user_input.lower() == "signup":
        username = input("Type Username: ")
        first_name = input("Type First Name: ")
        last_name = input("Type Last Name: ")
        while True:
            email = input("Type in your email address! ")
            if "@" not in email:
                print("Incorrect email address")
                continue
            else:
                 break 
         
        password = input("Type password in")

        #Hash the password here

        user = User_Profile(username,first_name, last_name, email, password)

        user_list[user.username]=(password)

        print(user_list[user.username])

    #ToDo this code can be simplified in the future
    if user_input.lower() == "login":
        registered_user = input("Input username: ")
        while True:
            if registered_user not in user_list.keys():
                print("Not registered, try again")
                continue
            else:
                break

        registered_password = input("Type password")

        # Here I will check the hash of the password to see if it matches registered_password

        while True:
            if registered_password not in user_list[registered_user]:
                print("Incorrect password, try again")
                continue
            else:
                break
        print ("Successful login")
    



        
