import unittest
from unittest.mock import patch
import sys
import os
import random
import string
import time

# Add the 'src' directory to the sys.path to make all modules inside it accessible.
## This will be changed later to import from github or another method
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/user')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/db')))
from db_functions import * 
from user_login import create_signup, create_login

def generate_username():
    adjectives = ['fast', 'cool', 'happy', 'lazy', 'brave', 'fuzzy', 'sneaky', 'loud']
    nouns = ['tiger', 'panda', 'ninja', 'robot', 'wizard', 'penguin', 'dragon', 'sloth']
    suffixes = ['x', '123', '_dev', '99', 'bot', '_01', '_zz']

    prefix = "test_"
    adj = random.choice(adjectives)
    noun = random.choice(nouns)
    suffix = random.choice(suffixes)
    number = ''.join(random.choices(string.digits, k=2))

    username = f"{prefix}{adj}_{noun}{suffix}{number}"

    if len(username) > 16:
        username = username[:16]

    return username

def delete_test_users():
    delete_query = "DELETE FROM users WHERE username LIKE 'test_%';"
    delete_data(delete_query)
    print("Deleting test users")


class TestUserCreation(unittest.TestCase):
    # For the test to work I just need to make sure I have a static user already in the DB

    def setUp(self):
        self.static_user = ("logintestuser123","Test","User","testuser@gmail.com","test_user_123")
        self.elastic_user = (generate_username(),"Test","User","testuser@gmail.com","test_user_123")
        self.bad_fn = (generate_username(),"123","User","testuser@gmail.com","test_user_123")
        self.bad_ln = (generate_username(),"Test","123","testuser@gmail.com","test_user_123")
        self.bad_email = (generate_username(),"Test","123","testusermail.com","test_user_123")
        self.bad_fields = ("logintestuser123","345","123","testusermail.com","pass")
        self.test_user_1= create_signup(*self.elastic_user)
    

    def test_user_creation(self):
       print("Creating Test User: \n\n\n")
       self.assertTrue(*self.test_user_1)

    def test_user_exist(self):
        print("Checking if user exists \n\n\n")
        _, errors = create_signup(*self.static_user)
        self.assertIn("username", errors)
    
    def test_bad_first_name(self):      
        print("Bad first name test:")
        _, errors = create_signup(*self.bad_fn)
        self.assertIn("first_name", errors)
        
    def test_bad_last_name(self):      
        print("Bad last name test:")
        _, errors = create_signup(*self.bad_ln)
        self.assertIn("last_name", errors)
    
    def test_bad_email(self):
        print("Testing email")
        _, errors = create_signup(*self.bad_email)
        self.assertIn("email",errors)

    def test_bad_multiple_fields(self):
        print("Testing multiple bad fields")
        _, errors = create_signup(*self.bad_fields)
        self.assertIn("username",errors)
        self.assertIn("first_name",errors)
        self.assertIn("last_name",errors)
        self.assertIn("email",errors)
        self.assertIn("password",errors)
    
    def test_login(self):
        print("Logging in")
        login_attempt = create_login("logintestuser123","test_user_123")
        self.assertTrue(login_attempt)

    def test_bad_login_password(self):
        print("Testing bad password")
        login_attempt = create_login("logintestuser123","test123")
        self.assertIsNone(login_attempt)

    def test_bad_login_username(self):
        print("Testing bad username")
        login_attempt = create_login("testuser10234","test123")
        self.assertIsNone(login_attempt)


if __name__ == '__main__':
    unittest.main(exit=False)
    delete_test_users()
