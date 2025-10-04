import unittest
import os
import sys
from tests.conftest import client, json_users
import pytest
import io

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.language_modifier.text_file_translator import TextFileTranslator

test_file_1 = "testfile.txt"
test_file_2 = "testfile2.txt"
test_file_3 = "testfile3.txt"

test_dir = os.path.join(os.path.dirname(__file__), "") 
os.makedirs(test_dir, exist_ok=True)

@pytest.fixture(scope="session",autouse=True)
def create_txt_file():
    with open(os.path.join(test_dir, test_file_1), "w") as f:
        f.write("This is a test file.")
    with open(os.path.join(test_dir, test_file_2), "w") as f:
        f.write("This is a test file with a comma\nSecond line 1,2,3\nThird line")
    with open(os.path.join(test_dir, test_file_3), "w") as f:
        f.write("This is a test file\n\nBlank line above this")

class TestUserInput(unittest.TestCase):
    # These test cases test the unique file name functionality
    @classmethod
    def setUpClass(cls,json_users):
        create_txt_file()
        user_1, _ = json_users
        cls.file_1 = TextFileTranslator(test_file_1, "Spanish", test_dir,user_1.username)
        cls.fake_file = TextFileTranslator("FakeFile.txt", "Spanish", test_dir,user_1.username)
        cls.file_2 = TextFileTranslator(test_file_2, "Hindi", test_dir,user_1.username)
        cls.file_3 = TextFileTranslator(test_file_3, "Hindi", test_dir,user_1.username)

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

class TestJsonFields:

    def test_json_txt_file(self, client,json_users):
        user_1, _ = json_users
        file_data = {
            "file": (io.BytesIO(b"dummy content"), "testfile.txt"),
            "target_language": "French"
        }

        response_send_file = client.post(
            "/translate_document",
            data=file_data,
            content_type="multipart/form-data",
            headers={"Authorization": f"Bearer {user_1.token}"}
        )

        assert response_send_file.status_code == 200
    
    def test_json_bad_txt_file(self, client, json_users):
        
        user_1, _ = json_users

        bad_file_data = {
            "file": (io.BytesIO(b"dummy content"), "testfile.fakeext"),
            "target_language": "French"
        }

        response_send_bad_file = client.post(
            "/translate_document",
            data=bad_file_data,
            content_type="multipart/form-data",
            headers={"Authorization": f"Bearer {user_1.token}"}
        )

        assert response_send_bad_file.status_code == 400

    def test_json_download_txt_file(self, client, json_users):
        user_1, _ = json_users
        response_download_file = client.get(
            "/download_file?file=testfile.txt",
            headers={"Authorization": f"Bearer {user_1.token}"}   
        )

        assert response_download_file.status_code == 200

    def test_json_download_bad_txt_file(self, client, json_users):
        user_1, _ = json_users
        response_bad_download = client.get(
            "/download_file?file=file_doesnt_exist.txt",
            headers={"Authorization": f"Bearer {user_1.token}"}   
        )
    
        assert response_bad_download.status_code == 400
    
    def test_json_download_bad_txt_ext(self, client, json_users):
        user_1, _ = json_users
        response_bad_download = client.get(
            "/download_file?file=bad_txt_ext.bubble",
            headers={"Authorization": f"Bearer {user_1.token}"}   
        )
    
        assert response_bad_download.status_code == 400

    def test_json_bad_upload_txt_file(self, client, json_users):
        user_1, _ = json_users

        response_bad_upload = client.post(
        "/translate_document",
        data = {
            "file": (io.BytesIO(b"dummy content"), "file_doesnt_exist.txt"),
            "target_language": "French"
        },
        content_type="application/json",
        headers={"Authorization": f"Bearer {user_1.token}"})

        assert response_bad_upload.status_code == 400



