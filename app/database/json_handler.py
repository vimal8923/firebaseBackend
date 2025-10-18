import json

FILE_PATH = "users.json"

def read_users():
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def write_users(users):
    with open(FILE_PATH, "w") as f:
        json.dump(users, f, indent=4)
