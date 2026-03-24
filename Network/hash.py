import os
import json
from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv

load_dotenv()


def _get_cipher() -> Fernet:
    """Create and return the Fernet cipher from the environment key."""
    key = os.environ.get("WIFI_SECRET_KEY")
    if not key:
        raise RuntimeError("WIFI_SECRET_KEY environment variable is not set")
    return Fernet(key.encode("utf-8"))


def encrypt_data(data: dict) -> str:
    """Encrypt a Python dict and return it as a string token."""
    cipher = _get_cipher()
    json_data = json.dumps(data, ensure_ascii=False)
    token = cipher.encrypt(json_data.encode("utf-8"))
    return token.decode("utf-8")


def decrypt_data(token: str) -> dict:
    """Decrypt a token string and return the original Python dict."""
    cipher = _get_cipher()
    try:
        decrypted = cipher.decrypt(token.encode("utf-8"))
    except InvalidToken as e:
        raise ValueError("Invalid encrypted token") from e

    try:
        return json.loads(decrypted.decode("utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError("Decrypted data is not valid JSON") from e


# Backward-compatible alias for older code
def unencrypt_data(token: str) -> dict:
    return decrypt_data(token)