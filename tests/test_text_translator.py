import unittest
import os
import glob
import time
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.language_modifier.text_file_translator import TextFileTranslator

test_file_1 = "testfile.txt"
test_file_2 = "testfile2.txt"
test_file_3 = "testfile3.txt"

test_dir = os.path.join(os.path.dirname(__file__), "") 
os.makedirs(test_dir, exist_ok=True)

def create_txt_file():
    with open(os.path.join(test_dir, test_file_1), "w") as f:
        f.write("This is a test file")
    with open(os.path.join(test_dir, test_file_2), "w") as f:
        f.write("This is a test file\nSecond line\nThird line")
    with open(os.path.join(test_dir, test_file_3), "w") as f:
        f.write("This is a test file\n\nBlank line above this")

def remove_test_files():
    for f in glob.glob(os.path.join(test_dir, "*.txt")):
        os.remove(f)

class TestUserInput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        create_txt_file()
        cls.file_1 = TextFileTranslator(test_file_1, "Spanish", test_dir)
        cls.fake_file = TextFileTranslator("FakeFile.txt", "Spanish", test_dir)
        cls.file_2 = TextFileTranslator(test_file_2, "Hindi", test_dir)
        cls.file_3 = TextFileTranslator(test_file_3, "Hindi", test_dir)

    def test_file_translation(self):
        output = self.file_1.save_txt_file()
        self.assertTrue(os.path.exists(os.path.join(test_dir, output)))

    def test_file_exists(self):
        self.file_1.save_txt_file()

        self.assertNotEqual(self.file_1.new_output_file, self.file_1.output_file)

    def test_file_not_valid(self):
        with self.assertRaises(FileNotFoundError):
            self.fake_file.save_txt_file()

    def test_multi_line_file(self):
        output = self.file_2.save_txt_file()
        self.assertTrue(os.path.exists(os.path.join(test_dir, output)))

    def test_blank_line(self):
        output = self.file_3.save_txt_file()
        self.assertTrue(os.path.exists(os.path.join(test_dir, output)))

if __name__ == "__main__":
    unittest.main(exit=False)
    print("Deleting test files in 20 seconds")
    time.sleep(20)
    remove_test_files()