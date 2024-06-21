import unittest
from models.user import generate_login_hash, User 
import datetime
import bcrypt
import base64
import hashlib

class TestUser(unittest.TestCase):
    """test user mode"""
    def setUp(self) -> None:
        deets1 = {'name':'Collins', 'master_pass':'password1', 'user_id':'32545-53535-53535'}
        self.User1 = User(**deets1)
        self.User2 = User({'name':'Kush', 'master_pass':'password2'})

    def test_object_types(self):
        """used to test the users types"""
        self.assertIsInstance(self.User1, User)
        self.assertIsInstance(self.User2, User)
        self.assertIsNot(self.User1, self.User2)

    def test_user1_details(self):
        """observing user1 details"""

        self.assertEqual(self.User1.name, 'Collins')
        self.assertEqual(type(self.User1.user_id), str)
        self.assertIsInstance(self.User1.date_joined, datetime.datetime)
        self.assertIsInstance(self.User1.date_updated, datetime.datetime)
        # testing hash
        passwd = base64.b64encode(hashlib.sha256('password1'.encode('utf-8')).digest())
        self.assertTrue(bcrypt.checkpw(passwd, generate_login_hash('password1')))

    # def test_null(self):
    #     """testing null imput"""
    #     User2 = User()
        