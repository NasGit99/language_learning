import pytest
from language_learning import create_app
import logging
import random


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture()
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

@pytest.fixture
def credentials():
    from test_user_login import TestJsonFields
    username = TestJsonFields.username
    password = TestJsonFields.password
    return username, password


@pytest.fixture(scope="session",autouse=True)
def cleanup_files():
    import time
    yield
    time.sleep(3)
    logging.info("Deleting test files")
    remove_test_files()