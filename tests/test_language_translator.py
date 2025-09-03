import unittest
from unittest.mock import AsyncMock, patch
import sys
import os
from tests.conftest import client
import json


# Add the 'src' directory to the sys.path to make all modules inside it accessible.
## This will be changed later to import from github
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/language_modifier/')))

from src.language_modifier.language_translator import translate_text

class TestTranslateText(unittest.IsolatedAsyncioTestCase):
    async def test_translate(self):
        result = await(translate_text('Hi','French'))
        self.assertTrue(result)

    async def test_bad_translate(self):
        with self.assertRaises(ValueError):
            await translate_text('Hi', 'BadFrench')

class TestJsonFields:
    import random
    username = f"test_{random.randint(1,10000)}"
    password = f"test_{random.randint(1,10000)}"

    def test_translate_json(self,client):
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

        response = client.post(
        "/translate_text",
        data=json.dumps({
            "user_text": "Hi this is billy from america",
            "target_language": "French",
        }),
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"})

        assert response.status_code == 200

        response_2= client.post(
        "/translate_text",
        data=json.dumps({
            "user_text": "Hi this is billy from america",
            "target_language": "fakelang",
        }),
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"})

        assert response_2.status_code == 400

        print (response.get_json(), response_2.get_json())


