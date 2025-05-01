import unittest
import sys
import os

## ToDo: Add code to test multiple languages
# ToDo: Add code to test bad language" 

# Add the 'src' directory to the sys.path to make all modules inside it accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/language_modifier/')))

# Now, you can import your module
from language_resource import validate_codes  # Import the function to be tested

class TestUserInput(unittest.TestCase):

    def test_valid_language(self):
        valid_language = 'English'

        self.assertTrue(validate_codes(valid_language))  

if __name__ == '__main__':
    unittest.main()
