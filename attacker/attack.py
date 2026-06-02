import random
import time
import requests

TARGET_URL = "http://backend:8000/login"

USERS = [
    "admin",
    "root",
    "tomas",
    "user",
]

PASSWORDS = [
    "123456",
    "password",
    "admin",
    "qwerty",
    "secret",
]

while True:
    payload = {
        "username": random.choice(USERS),
        "password": random.choice(PASSWORDS)
    }

    try:
        response = requests.post(
            TARGET_URL,
            json=payload,
            timeout=5
        )

        print(
            f"User={payload['username']} "
            f"Status={response.status_code}"
        )

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(1)