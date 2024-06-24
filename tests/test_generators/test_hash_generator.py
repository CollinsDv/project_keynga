from models.user import User
from models.generators import generate_login_hash
import unittest
import bcrypt
import base64

import hashlib


class TestHashGenerator(unittest.TestCase):
    """tests generate_login_hash"""
    def setUp(self) -> None:
        self.dictionary1 = {'name': 'Collins', 'master_pass': 'password1'}
        self.user1 = User(**self.dictionary1)

    def test_generate_login_hash(self):
        """Test that generate_login_hash produces a consistent hash"""
        password = "testpassword"
        to_hash = base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest())
        hashed_password = generate_login_hash(password)
        self.assertTrue(bcrypt.checkpw(to_hash, hashed_password),
                        "The hashed password does not match the original password")
        
    def test_user_hash(self):
        """testing the hash implementation with user"""
        user_hash = base64.b64encode(hashlib.sha256(self.dictionary1['master_pass'].encode('utf-8')).digest())
        self.assertTrue(bcrypt.checkpw(user_hash, self.user1.hash_pw))

if __name__ == '__main__':
    unittest.main()