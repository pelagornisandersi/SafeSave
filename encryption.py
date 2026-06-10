import base64
import os

from cryptography.fernet import Fernet

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from cryptography.hazmat.primitives import hashes


# derive encryption key
def generate_key(master_password, salt):

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )

    key = base64.urlsafe_b64encode(
        kdf.derive(master_password.encode())
    )

    return key


# encrypt
def encrypt_password(password, master_password, salt):

    key = generate_key(master_password, salt)

    cipher = Fernet(key)

    encrypted = cipher.encrypt(password.encode())

    return encrypted.decode()


# decrypt
def decrypt_password(encrypted_password, master_password, salt):

    key = generate_key(master_password, salt)

    cipher = Fernet(key)

    decrypted = cipher.decrypt(
        encrypted_password.encode()
    )

    return decrypted.decode()