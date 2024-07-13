import hashlib
import bcrypt
import base64
"""generates a hash for the user password
"""


def generate_login_hash(password):
    """generate an strong irreverable hash

    prevents passwords above 72bytes from being ignored by bcrypt
    Return:
        obj (str): the hashed value
    """
    if not password:
        print('provide a password')
    # Convert string into binary form for crypto processing
    binary = password.encode('utf-8')
    # sha256 ciphertext genration
    sha_pw = hashlib.sha256(binary).digest()

    # encoding to preventing NULL byte problems before bycrypt hashing
    encoded = base64.b64encode(sha_pw)
    hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())

    return hashed


def verify_password(user_pass, hash):
    """used to verify a user on login"""
    encoded = base64.b64encode(hashlib.sha256(user_pass.encode()).digest())
    return bcrypt.checkpw(encoded, hash.encode())


if __name__ == '__main__':
    user_pass = True
    while user_pass:
        master_pass = input('enter master password: ')
        if len(master_pass) <= 0:
            print('enter your password')
            continue
        generate_login_hash(master_pass)
        break
