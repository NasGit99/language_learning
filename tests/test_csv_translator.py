from tests.conftest import client, json_users
import os 
import csv
import io
import pytest


test_dir = os.path.join(os.path.dirname(__file__)) 

test_file_1 = "testfile.csv"
test_file_2 = "testfile2.csv"
test_file_3 = "testfile3.csv"

test_file_1_data = [
    ['Name', 'Class', 'Hobby'],
    ['Billy', 'Science', "Going outside"],
    ['Sally', 'Math', 'Playing basketball']
]

test_file_2_data = [
    ['Name', 'Class', 'Hobby'],
    ['Billy,', 'Science:', "Going.., outside!"],
    ['Sally','@#@$', 'Playing basketball'],
    ['Gres', '123,456,679', 'Shopping for new clothes']
]

test_file_3_data = [
    ['Name', 'Class', 'Hobby'],
    ['', '', " "],
    ['Sally', '', 'Playing basketball'],
    ['Gres', 'Math', 'Shopping for new clothes'],
    ['', 'Math', 123]
]

@pytest.fixture(scope="session",autouse=True)
def create_csv_file():
    with open(os.path.join(test_dir, test_file_1), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(test_file_1_data)
    with open(os.path.join(test_dir, test_file_2), "w") as f:
        writer = csv.writer(f)
        writer.writerows(test_file_2_data)
    with open(os.path.join(test_dir, test_file_3), "w") as f:
        writer = csv.writer(f)
        writer.writerows(test_file_3_data)

class Test_CSV_Translator():

    # test_text_translator test most of the upload and download functionality so not much is needed here besides
    # the file translation for the samples we have

    def test_csv_creation(self, client, json_users):
        user_1, _ = json_users

        file_data = {
            "file": (io.BytesIO(b"dummy content"), "testfile.csv"),
            "target_language": "French"
        }

        response_send_file = client.post(
            "/translate_document",
            data=file_data,
            content_type="multipart/form-data",
            headers={"Authorization": f"Bearer {user_1.token}"}
        )

        assert response_send_file.status_code == 200
    
    def test_csv_creation_nums_with_commas(self, client, json_users):
        user_1, _ = json_users

        file_data = {
            "file": (io.BytesIO(b"dummy content"), "testfile2.csv"),
            "target_language": "French"
        }

        response_send_file = client.post(
            "/translate_document",
            data=file_data,
            content_type="multipart/form-data",
            headers={"Authorization": f"Bearer {user_1.token}"}
        )

        assert response_send_file.status_code == 200
        
    def test_csv_creation_nums_and_blanks(self, client, json_users):
        user_1, _ = json_users

        file_data = {
            "file": (io.BytesIO(b"dummy content"), "testfile3.csv"),
            "target_language": "French"
        }

        response_send_file = client.post(
            "/translate_document",
            data=file_data,
            content_type="multipart/form-data",
            headers={"Authorization": f"Bearer {user_1.token}"}
        )

        assert response_send_file.status_code == 200

    def test_json_download_csv_file(self, client, json_users):
        user_1, _ = json_users
        response_download_file = client.get(
            "/download_file?file=testfile.csv",
            headers={"Authorization": f"Bearer {user_1.token}"}   
        )

        assert response_download_file.status_code == 200