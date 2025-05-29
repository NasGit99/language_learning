import unittest
from unittest import mock
from unittest.mock import patch
import sys
import os

## ToDo: Add code to test multiple languages
# ToDo: Add code to test bad language" 

# Add the 'src' directory to the sys.path to make all modules inside it accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/language_modifier/')))

from language_code_resource import validate_codes

class TestUserInput(unittest.TestCase):

    def test_valid_language(self):
        valid_language = 'English'

        self.assertTrue(validate_codes(valid_language))  

    @patch('builtins.input', side_effect=['exit'])
    def test_invalid_language(self, mocked_input):
        result = validate_codes('FakeLang')
        self.assertIsNone(result)
    

if __name__ == '__main__':
    unittest.main()
