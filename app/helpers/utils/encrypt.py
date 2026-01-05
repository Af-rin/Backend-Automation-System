from cryptography.fernet import Fernet
from app.core.config import settings

# encryption key
KEY = settings.ENCRYPTION_KEY
cipher_suite = Fernet(KEY)

# to encrypt
def encrypt(data: str) -> str:
    encrypted = cipher_suite.encrypt(data.encode())
    return encrypted.decode()

# to decrypt
def decrypt(data: str) -> str:
    decrypted = cipher_suite.decrypt(data.encode())
    return decrypted.decode()

def is_encryption_required(url: str) -> bool:
    # Protected urls
    required_urls = ["/register", "/login", "/logout"]
    return any(required_url in url for required_url in required_urls)