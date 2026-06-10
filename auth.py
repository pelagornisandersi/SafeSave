import bcrypt
import os

MASTER_FILE = "master.hash"
SALT_FILE = "salt.bin"


# setup master password
def setup_master_password(password):

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    with open(MASTER_FILE, "wb") as file:
        file.write(hashed)

    # generate salt
    salt = os.urandom(16)

    with open(SALT_FILE, "wb") as file:
        file.write(salt)


# verify password
def verify_master_password(password):

    with open(MASTER_FILE, "rb") as file:
        stored_hash = file.read()

    return bcrypt.checkpw(
        password.encode(),
        stored_hash
    )


# check setup
def master_password_exists():

    return os.path.exists(MASTER_FILE)


# load salt
def load_salt():

    with open(SALT_FILE, "rb") as file:
        return file.read()