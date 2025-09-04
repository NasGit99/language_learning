import sys
import os
import random
import string
import json

from tests.conftest import client, json_users

# Add the 'src' directory to the sys.path to make all modules inside it accessible.
## This will be changed later to import from github or another method
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/user')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/db')))
from db_functions import * 
from user.user_login import UserProfile

def generate_username():
    adjectives = ['fast', 'cool', 'happy', 'lazy', 'brave', 'fuzzy', 'sneaky', 'loud']
    nouns = ['tiger', 'panda', 'ninja', 'robot', 'wizard', 'penguin', 'dragon', 'sloth']
    suffixes = ['x', '123', '_dev', '99', 'bot', '_01', '_zz']

    prefix = "test_"
    adj = random.choice(adjectives)
    noun = random.choice(nouns)
    suffix = random.choice(suffixes)
    number = ''.join(random.choices(string.digits, k=2))

    username = f"{prefix}{adj}_{noun}{suffix}{number}"

    return username[:16]

def create_token(client, username, password, refresh=False):
    response = client.post("/login", json={
        "username": username,
        "password": password
    })
    assert response.status_code == 200
    data = response.get_json()
    return data if refresh else data["access_token"]


class TestUserCreation:
    # For the test to work I just need to make sure I have a static user already in the DB
    static_user= UserProfile("logintestuser123","testuser@gmail.com","Test","User","test_user_123")
    elastic_user = UserProfile(generate_username(),"testuser@gmail.com","Test","User","test_user_123")
    bad_fn = UserProfile(generate_username(),"testuser@gmail.com","123","User","test_user_123")
    bad_ln = UserProfile(generate_username(),"testuser@gmail.com","Test","123","test_user_123")
    bad_email = UserProfile(generate_username(),"testusermail.com","Test","123","test_user_123")
    bad_fields = UserProfile("logintestuser123","testusermail.com","345","123","pass")
    test_user_1= UserProfile(elastic_user.username, elastic_user.email, elastic_user.first_name, 
                                      elastic_user.last_name, elastic_user.password)
    def test_user_creation(self):
       print("Creating Test User: \n\n\n")
       username, _ = self.test_user_1.create_signup()
       assert username

    def test_user_exist(self):
        print("Checking if user exists \n\n\n")
        _, errors = self.static_user.create_signup()
        assert "username" in errors
    
    def test_bad_first_name(self):      
        print("Bad first name test:")
        _, errors = self.bad_fn.create_signup()
        assert "first_name" in errors
        
    def test_bad_last_name(self):      
        print("Bad last name test:")
        _, errors = self.bad_ln.create_signup()
        assert "last_name" in errors
    
    def test_bad_email(self):
        print("Testing email")
        _, errors = self.bad_email.create_signup()
        assert "email" in errors

    def test_bad_multiple_fields(self):
        print("Testing multiple bad fields")
        _, errors = self.bad_fields.create_signup()
        assert "username" in errors
        assert "first_name" in errors
        assert "last_name"in errors
        assert "email" in errors
        assert "password"in errors
    
    def test_login(self):
        print("Logging in")
        login_attempt = UserProfile.create_login("logintestuser123","test_user_123")
        assert login_attempt

    def test_bad_login_password(self):
        print("Testing bad password")
        login_attempt = UserProfile.create_login("logintestuser123","test123")
        assert login_attempt is None

    def test_bad_login_username(self):
        print("Testing bad username")
        login_attempt = UserProfile.create_login("testuser10234","test123")
        assert login_attempt is None

class JsonUser:
    def __init__(self,client, username = None, password = None, refresh = None):
        self.username = username or generate_username() 
        self.password = password or f"test{random.randint(1,10000)}" or password 
        self.token = create_token(client, self.username, self.password, refresh)

class TestJsonFields():
        
    def create_user(self,client,username, password):
        response = client.post(
        "/signup",
        data=json.dumps({
            "username": f"{username}",
            "first_name": "cakes",
            "last_name": "cake",
            "email": "darktest@gmail.com",
            "password": f"{password}",
        }),
        content_type="application/json")
        return response

    def test_create_user_json(self, client, json_users):
        user1, _ = json_users

        response = self.create_user(client,user1.username, user1.password)
       
        assert response.status_code == 200

        assert user1.token is not None
    
    def test_login_user_json(self,client,json_users):
        _, user2 = json_users
        response = client.post(
        "/login",
        data=json.dumps({
            "username": f"{user2.username}",
            "password": f"{user2.password}",
        }),
        content_type="application/json")

        token = user2.token
        print(token)
        access_token = token["access_token"]
        refresh_token = token["refresh_token"]

        assert response.status_code == 200
        assert access_token is not None
        assert refresh_token is not None

    def test_profile_json(self,client,json_users):

        user1, _ = json_users
        
        response = client.get(
            "/profile",
            headers={"Authorization": f"Bearer {user1.token}"}
        )
        assert response.status_code == 200

        data = response.get_json()
        assert "User Profile" in data
        assert "Translation_history" in data
        assert "File_translation_history" in data

        print(data)

    def update_profile(self,client,json,token):

        response = client.patch(
        "/update_profile",
        headers={"Authorization": f"Bearer {token}"},
        data = json,
        content_type="application/json"
          ) 
        
        msg = response.get_json()
        print(msg)

        return response    

    def test_update_profile_badpw_json(self,client,json_users):
        user1, _ = json_users
        data = json.dumps({
            "new_password": f"{user1.password}",
        })
        response = self.update_profile(client,data,user1.token)

        assert response.status_code == 400

    def test_update_profile_goodpw_json(self, client):

        # For this test case a new user is required to not mess with previous test cases

        username = generate_username()
        old_password = "profiletest123"
        new_password = "newpw123"

        self.create_user(client,username,old_password)

        tokens = create_token(client, username, old_password, refresh = True)
        access_token = tokens["access_token"]

        data = json.dumps({
            "old_password": old_password,
            "new_password": new_password
        })
        response = self.update_profile(client, data, access_token)
        assert response.status_code == 200
    
    def test_update_profile_username_json(self, client):
        old_username = generate_username()
        password = "startpw123"
        new_username = f"{old_username[:12]}_new"

        self.create_user(client,old_username,password)

        tokens = create_token(client, old_username, password, refresh=True)
        access_token = tokens["access_token"]

        data = json.dumps({"new_username": new_username})
        response = client.patch(
            "/update_profile",
            headers={"Authorization": f"Bearer {access_token}"},
            data=data,
            content_type="application/json"
        )

        assert response.status_code == 200
        resp_json = response.get_json()
        assert "updated_fields" in resp_json
        assert "username" in resp_json["updated_fields"]
        assert "new_access_token(1 hour) due to name change" in resp_json
        assert resp_json["msg"] == "Request a refresh token through the /login endpoint for longer access"

        new_tokens = create_token(client, new_username, password, refresh=True)
        assert "access_token" in new_tokens