import base64
from dataclasses import dataclass
import json
import string
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import hmac
import hashlib
import sqlite3

"""
CREATE TABLE users (
    username TEXT NOT NULL PRIMARY KEY,
    password TEXT NOT NULL,
    session_id TEXT
);
"""


@dataclass
class AuthBody:
    username: str
    password: str


def create_user(username: str, password: str, refresh_token: str) -> None:
    conn = sqlite3.connect("password_database.db")
    cursor = conn.cursor()

    cursor.execute(
        f"INSERT INTO users (username, password, session_id) VALUES ('{username}', '{password}', '{refresh_token}');",
    )

    conn.commit()

def validate_user(username: str, password: str) -> bool:
    conn = sqlite3.connect("password_database.db")
    cursor = conn.cursor()

    cursor.execute(
        f"SELECT * FROM users where username = '{username}' and password = '{password}';",
    )

    rows = cursor.fetchall()

    if len(rows) == 0:
        print("Invalid username or password")
        return False

    return True

def update_refresh_token(username: str, password: str, refresh_token: str) -> None:
    conn = sqlite3.connect("password_database.db")
    cursor = conn.cursor()

    cursor.execute(
        f"Update users set session_id = '{refresh_token}' where username = '{username}';",
    )

def get_refresh_token(username: str) -> str:
    # Using in-memory database
    # returns active refresh token, if found
    conn = sqlite3.connect("password_database.db")
    cursor = conn.cursor()

    cursor.execute(
        f"SELECT session_id FROM users where username = '{username}';",
    )

    rows = cursor.fetchall()

    if rows[0][0] is None:
        print("No active session")
        return 0

    return rows[0][0]


def generate_jwt_token(username: str, expiry_time) -> str:
    expiry_time = str(datetime.now() + timedelta(minutes=expiry_time))
    signature_algorithm = "AES"

    signature_algorithm_object = json.dumps({"alg": signature_algorithm, "typ": "JWT"})
    user_data_object = json.dumps({"username": username, "expiry_time": expiry_time})

    signature_algorithm_object_encoded = base64.b64encode(
        bytes(signature_algorithm_object, "utf-8")
    ).decode()
    user_data_encoded = base64.b64encode(bytes(user_data_object, "utf-8")).decode()

    signature = sign_jwt_token(
        f"{signature_algorithm_object_encoded}.{user_data_encoded}"
    )

    return f"{signature_algorithm_object_encoded}.{user_data_encoded}.{signature}"


def sign_jwt_token(token: str) -> str:
    # Hash the token including the secret key, this function should be dependent on the signing alogorithm in jwt

    with open(".env/secret.txt", "r") as f:
        secret_key = f.read().strip().encode()

    signature = hmac.new(secret_key, token.encode(), hashlib.sha256).digest()

    return base64.urlsafe_b64encode(signature).decode()


def validate_jwt_token(token: str) -> int:
    if token is None:
        return -1

    tokens = token.split(".")
    user_data_decoded = json.loads(base64.b64decode(tokens[1]).decode())

    timedelta = datetime.now() > datetime.strptime(
        user_data_decoded["expiry_time"], "%Y-%m-%d %H:%M:%S.%f"
    )

    if timedelta:
        print("Token Expired")
        return -2

    signature = sign_jwt_token(f"{tokens[0]}.{tokens[1]}")

    if signature == tokens[2]:
        print("Valid token")
        return 0
    else:
        print("Invalid token")
        return -1
