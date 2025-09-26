import random
import string

def generate_string():
    adjectives = ['fast', 'cool', 'happy', 'lazy', 'brave', 'fuzzy', 'sneaky', 'loud']
    nouns = ['tiger', 'panda', 'ninja', 'robot', 'wizard', 'penguin', 'dragon', 'sloth']
    suffixes = ['x', '123', '_dev', '99', 'bot', '_01', '_zz']

    prefix = "test_"
    adj = random.choice(adjectives)
    noun = random.choice(nouns)
    suffix = random.choice(suffixes)
    number = ''.join(random.choices(string.digits, k=2))

    new_string = f"{prefix}{adj}_{noun}{suffix}{number}"

    return new_string

def generate_username():
    username = generate_string()
    return username[:16]

def generate_password():
    password = generate_string()
    return password

def create_token(client, username, password, refresh=False):
    response = client.post("/login", json={
        "username": username,
        "password": password
    })
    data = response.get_json()
    return data if refresh else data["access_token"]

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