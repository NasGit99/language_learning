import pytest
from language_learning import create_app
import logging
import os


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "TESTING_FOLDER" : os.path.join(os.getcwd(), 'tests')
    })
    yield app

@pytest.fixture(scope="session")
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def remove_test_files():
    import glob
    import os
    test_dir = os.path.join(os.path.dirname(__file__), "") 
    os.makedirs(test_dir, exist_ok=True)

    for f in glob.glob(os.path.join(test_dir, "*.txt")):
        os.remove(f)

@pytest.fixture(scope="session",autouse=True)
def cleanup_files():
    import time
    yield
    time.sleep(3)
    logging.info("Deleting test files")
    remove_test_files()

@pytest.fixture(scope="session",autouse=True)
def delete_test_users():
    yield
    from src.db.db_functions import delete_data
    delete_query = "DELETE FROM users WHERE username LIKE 'test%';"
    delete_data(delete_query)
    print("Deleting test users")

@pytest.fixture(scope="session")
def json_users(request):
    client = request.getfixturevalue("client")

    from tests.helpers import JsonUser
    user1 = JsonUser(client)
    user2 = JsonUser(client, username=user1.username, password=user1.password, refresh=True)
    return user1, user2