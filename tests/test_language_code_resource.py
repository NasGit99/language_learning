import unittest
from unittest.mock import patch
import sys
import os

# Add the 'src' directory to the sys.path to make all modules inside it accessible.
## This will be changed later to import from github or another method
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/language_modifier/')))

from language_code_resource import validate_codes

class TestUserInput(unittest.TestCase):

    def test_valid_language(self):
        print("Test valid language")
        print("---------------------------\n\n")
        with patch('builtins.input', return_value='English'):
            result = validate_codes()
            self.assertEqual(result, 'en')
        print("\n\n")
    
    def test_invalid_then_valid_input(self):
        print("Test invalid then valid language\n\n")
        with patch('builtins.input', side_effect=['Klingon', 'Spanish']):
            result = validate_codes()
            self.assertEqual(result, 'es')
        print("\n\n")
    
    def test_exit(self):
        print("Test exit function\n\n")
        with patch('builtins.input',return_value='Exit'):
            result = validate_codes()
            self.assertIsNone(result,'Exit')
        print("\n\n")
    
    def test_multiple_languages(self):
        print("Test multiple languages\n\n")
        with patch('builtins.input', side_effect=['English','Spanish','French','German']):
            result1 = validate_codes()
            result2 = validate_codes()
            result3 = validate_codes() 
            result4 = validate_codes()

            self.assertEqual(result1, 'en')
            self.assertEqual(result2, 'es')
            self.assertEqual(result3, 'fr')
            self.assertEqual(result4, 'de')
        print("\n\n")

if __name__ == '__main__':
    unittest.main()
