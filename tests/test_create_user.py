import unittest
from unittest.mock import patch
import sys
import os

# Add the 'src' directory to the sys.path to make all modules inside it accessible.
## This will be changed later to import from github or another method
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/user')))

from create_user import User_Profile
user = User_Profile("testuser","Billy","Bob","billybob@gmail.com")

class TestUserCreation(unittest.TestCase):

    def test_user(self):
        self.assertTrue(user)
        print("User Details:\n")
        for attr, value in user.__dict__.items():
            print(attr,":", value)
    
    def test_modify_profile(self):
        user.modify_profile("username", "billybob2")
        print("New username is:", user.username)
        self.assertEqual(user.username, "billybob2")
    
    def test_modify_profile_spaces(self):
        user.modify_profile("first name","josh")
        self.assertEqual(user.first_name,"josh")
        
    def test_modify_profile_error(self):
        with self.assertRaises(AssertionError):
            user.modify_profile("fakefield", "billybob2")
            
if __name__ == '__main__':
    unittest.main()
