import random
from tests.test_user_login import generate_username, create_token 

class JsonUser:
    def __init__(self, client, username=None, password=None, refresh=None):
        self.username = username or generate_username()
        self.password = password or f"test{random.randint(1,10000)}"

        client.post("/signup", json={
            "username": self.username,
            "first_name": "Test",
            "last_name": "User",
            "email": f"{self.username}@test.com",
            "password": self.password
        })
        
        self.token = create_token(client, self.username, self.password, refresh)