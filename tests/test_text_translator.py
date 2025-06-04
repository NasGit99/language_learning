import unittest
from unittest.mock import patch
import sys
import os
import time
import glob

# Add the 'src' directory to the sys.path to make all modules inside it accessible.
## This will be changed later to import from github or another method
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/language_modifier/')))

from text_translator import *

test_file_1 ="testfile.txt"
test_language_1 = "Spanish"
test_file_2 ="testfile2.txt"
test_language_2= "Hindi"

def create_txt_file():
    with open(test_file_1, "w") as file:
        file.write("This is a test file")
    
    with open(test_file_2, "w") as file:
        file.write("This is a test file\n This is the second line for the test file \n This is the third line")


def remove_test_files():
    for file_path in glob.glob("*.txt"):
        os.remove(file_path)
        print(f"Removed: {file_path}")

class TestUserInput(unittest.TestCase):

    def test_file_translation(self):
        create_new_file(test_file_1,test_language_1)     
        self.assertTrue(os.path.exists('Spanish_testfile.txt'))

    def test_file_exists(self):
        create_new_file(test_file_1,test_language_1)
        self.assertRaises(FileExistsError)
        self.assertTrue(os.path.exists('SPanish_testfile_1.txt'))
    
    def test_file_not_valid(self):
        create_new_file("FakeFile.txt",test_language_1)
        self.assertRaises(FileNotFoundError)
    
    def test_multi_line_file(self):
        create_new_file(test_file_2,test_language_2)
        self.assertTrue(os.path.exists('Hindi_testfile2.txt'))
        
    ## ToDo, Test multi line files

if __name__ == '__main__':
    create_txt_file()
    unittest.main(exit=False)
    time.sleep(15)
    print("Deleting test files in 15 seconds")
    remove_test_files()
