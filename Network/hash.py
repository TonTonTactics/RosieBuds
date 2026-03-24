import os
import json
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get("WIFI_SECRET_KEY")
if not key:
    raise ValueError("WIFI_SECRET_KEY environment variable is not set")

cipher = Fernet(key.encode())

def encrypt_data(data: dict) -> str:
    """Encrypt a Python dict and return as string"""
    json_data = json.dumps(data)
    return cipher.encrypt(json_data.encode()).decode()

def unencrypt_data(token: str) -> dict:
    """Decrypt a string and return Python dict"""
    decrypted = cipher.decrypt(token.encode())
    return json.loads(decrypted.decode())