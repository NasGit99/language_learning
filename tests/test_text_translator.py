import unittest
import os
import sys
from tests.conftest import client
import json
import io

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

class TestJsonFields:
    #ToDO: we can import the user1 json user in order to make the necessary request needed and split up the test cases
    import random
    username = f"test{random.randint(1,10000)}"
    password = f"test{random.randint(1,10000)}"

    def test_json_txt_file(self, client):
        # I will refactor this to make the default user easier to make
        # Also the test cases can be seperated
        token = client.post(
        "/signup",
        data=json.dumps({
            "username": f"{self.username}",
            "first_name": "cakes",
            "last_name": "cake",
            "email": "darktest@gmail.com",
            "password": f"{self.password}",
        }),
        content_type="application/json")
        token_data = token.get_json()

        access_token = token_data["access_token"]

        file_data = {
            "file": (io.BytesIO(b"dummy content"), "testfile.txt"),
            "target_language": "French"
        }

        response_send_file = client.post(
            "/translate_document",
            data=file_data,
            content_type="multipart/form-data",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        assert response_send_file.status_code == 200

        bad_file_data = file_data = {
            "file": (io.BytesIO(b"dummy content"), "testfile.fakeext"),
            "target_language": "French"
        }

        response_send_bad_file = client.post(
            "/translate_document",
            data=bad_file_data,
            content_type="multipart/form-data",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        assert response_send_bad_file.status_code == 400


        response_download_file = client.get(
            "/download_file?file=test_file.txt",
            headers={"Authorization": f"Bearer {access_token}"}   
        )

        assert response_download_file.status_code == 200

        response_bad_download = client.get(
            "/download_file?file=file_doesnt_exist.txt",
            headers={"Authorization": f"Bearer {access_token}"}   
        )
        
        assert response_bad_download.status_code == 400

        response_bad_upload = client.post(
        "/translate_document",
        data=json.dumps({
            "file": "file_doesnt_exist.txt",
            "target_language": "French",
        }),
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"})

        assert response_bad_upload.status_code == 400



