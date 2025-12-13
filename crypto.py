import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1_200_000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))

def encrypt_data(data: str, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(data.encode('utf-8'))


def decrypt_data(encrypted: bytes, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(encrypted).decode('utf-8')


# import os

# salt = os.urandom(16)
# password = "my_master_password"

# key = derive_key(password, salt)
# encrypted = encrypt_data("secret data", key)
# decrypted = decrypt_data(encrypted, key)

# print(decrypted)  # should print: secret data

# # Test wrong password fails
# wrong_key = derive_key("wrong_password", salt)
# try:
#     decrypt_data(encrypted, wrong_key)
# except Exception as e:
#     print(f"Correctly failed: {e}")
